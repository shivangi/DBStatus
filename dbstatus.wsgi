import web
import psycopg2
import decimal
import jsonpickle
import csv
import re
from web import form


# Needed to find the templates
import sys, os,traceback
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

from Utility import KLPDB


urls = (
     '/','getstatus',
     '/getdata/(.*)/(.*)','getData'
)


class DbManager:

  con = None
  cursor = None

  @classmethod
  def getMainCon(cls):
    if cls.con and cls.con.closed==0:
      pass
    else:
      cls.con = KLPDB.getConnection()
    return cls.con


statements = {"district_boundarycounts":"select b.name,bs.id,bs.count,bstu.scount,bstu.stucount,bass.progname,bass.assessname,bass.school_mapped_count,bass.school_assess_count,bass.student_assess_count from tb_boundary_schoolcount bs left outer join tb_boundary_studentcount bstu on (bs.id=bstu.id) left outer join tb_boundary_assessmentcount bass on (bs.id=bass.id),vw_boundary b where bs.id=b.id and b.boundary_category_id=%s",
"block_boundarycounts":"select b1.name,b.name,bs.id,bs.count,bstu.scount,bstu.stucount,bass.progname,bass.assessname,bass.school_mapped_count,bass.school_assess_count,bass.student_assess_count from tb_boundary_schoolcount bs left outer join tb_boundary_studentcount bstu on (bs.id=bstu.id) left outer join tb_boundary_assessmentcount bass on (bs.id=bass.id),vw_boundary b ,vw_boundary b1 where bs.id=b.id and b.parent_id=b1.id and b1.id=%s",
"cluster_boundarycounts":"select b2.name,b1.name,b.name,bs.id,bs.count,bstu.scount,bstu.stucount,bass.progname,bass.assessname,bass.school_mapped_count,bass.school_assess_count,bass.student_assess_count from tb_boundary_schoolcount bs left outer join tb_boundary_studentcount bstu on (bs.id=bstu.id) left outer join tb_boundary_assessmentcount bass on (bs.id=bass.id),vw_boundary b,vw_boundary b1 ,vw_boundary b2 where bs.id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and b1.id=%s",
               "schoolcounts":"select b2.name,b1.name,b.name,s.name,sstu.id,sstu.studentcount,sass.progname,sass.assessname,sass.student_assess_count from tb_schoolstudentcount sstu left outer join tb_schoolassessmentcount sass on (sstu.id=sass.id), vw_boundary b,vw_boundary b1, vw_boundary b2,vw_school s where sstu.id=s.id and s.boundary_id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and b.id=%s",
               "classcounts":"select b2.name,b1.name,b.name,s.name,ARRAY_TO_STRING(ARRAY[cstu.class,cstu.section],' '),cstu.id,cstu.studentcount,cass.progname,cass.assessname,cass.student_assess_count from tb_classstudentcount cstu left outer join tb_classassessmentcount cass on (cstu.id=cass.id), vw_boundary b,vw_boundary b1,vw_boundary b2,vw_school s where cstu.sid=s.id and s.boundary_id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and s.id=%s",
            "currentprograms":"select * from tb_currentprograms order by progname",
}
render_plain = web.template.render('templates/')

application = web.application(urls,globals()).wsgifunc()


def convertNone(value):
  if value==None: 
    return 0
  else:
    return value

class getstatus:
  def __init__(self):
    self.schoolcount={"scount":0,"stucount":0,"sstucount":0,"assessmentcount":{},"children":{}}
    self.preschoolcount={"scount":0,"stucount":0,"sstucount":0,"assessmentcount":{},"children":{}}
    self.currentprograms=[]
    self.updatedtime=""
  def getDistrictData(self,result,datacount):
      for row in result:
        name=row[0]
        id=row[1]
        scount=convertNone(row[2])
        sstucount=convertNone(row[3])
        stucount=convertNone(row[4])
        progname=row[5]
        assessname=row[6]
        smappedcount=convertNone(row[7])
        sassessedcount=convertNone(row[8])
        stuassessedcount=convertNone(row[9])

        if progname !=None and assessname!=None:
          if name in datacount["assessmentcount"]:
            if progname in datacount["assessmentcount"][name]:
              if assessname in datacount["assessmentcount"][name][progname]:
                datacount["assessmentcount"][name][progname][assessname]["smappedcount"]=datacount["assessmentcount"][name][progname][assessname]["smappedcount"]+smappedcount
                datacount["assessmentcount"][name][progname][assessname]["sassessedcount"]=datacount["assessmentcount"][name][progname][assessname]["sassessedcount"]+sassessedcount
                datacount["assessmentcount"][name][progname][assessname]["stuassessedcount"]=datacount["assessmentcount"][name][progname][assessname]["stuassessedcount"]+stuassessedcount
              else:
                datacount["assessmentcount"][name][progname][assessname]={"stuassessedcount":stuassessedcount,"sassessedcount":sassessedcount,"smappedcount":smappedcount}
            else:
              datacount["assessmentcount"][name][progname]={assessname:{"stuassessedcount":stuassessedcount,"sassessedcount":sassessedcount,"smappedcount":smappedcount}}
          else:
            datacount["assessmentcount"][name]={progname:{assessname:{"stuassessedcount":stuassessedcount,"sassessedcount":sassessedcount,"smappedcount":smappedcount}}}

          if name not in datacount["children"]:
            datacount["children"][name]={"id":id,"name":name,"scount":scount,"sstucount":sstucount,"stucount":stucount,"assessmentcount":{},"children":{}}
            datacount["scount"]=datacount["scount"]+scount
            datacount["sstucount"]=datacount["sstucount"]+sstucount
            datacount["stucount"]=datacount["stucount"]+stucount
        else:
            if name not in datacount["children"]:
              datacount["children"][name]={"id":id,"name":name,"scount":scount,"sstucount":sstucount,"stucount":stucount,"assessmentcount":{},"children":{}}
            datacount["scount"]=datacount["scount"]+scount
            datacount["sstucount"]=datacount["sstucount"]+sstucount
            datacount["stucount"]=datacount["stucount"]+stucount
     
      
  def GET(self):
    try:
      cursor = DbManager.getMainCon().cursor()
      cursor.execute(statements["district_boundarycounts"],(9,))
      result = cursor.fetchall()
      self.getDistrictData(result,self.schoolcount)

      cursor.execute(statements["district_boundarycounts"],(13,))
      result = cursor.fetchall()
      self.getDistrictData(result,self.preschoolcount)

      cursor.execute(statements['currentprograms'])
      result = cursor.fetchall()
      for row in result:
        self.currentprograms.append(row[0])

      cursor.execute("select to_char(self.updatedtime,'yyyy-mm-dd HH24:MI:SS') from tb_statusinfo")
      result=cursor.fetchall()
      for row in result:
       self.updatedtime=row[0]

      DbManager.getMainCon().commit()
      cursor.close()
    except:
      traceback.print_exc(file=sys.stderr)
      cursor.close()
      DbManager.getMainCon().rollback()


    statusinfo={"schoolcount":self.schoolcount,"preschoolcount":self.preschoolcount,"currentprograms":self.currentprograms,"updatedtime":self.updatedtime}
    print statusinfo

    web.header('Content-Type','text/html; charset=utf-8')
    return render_plain.dbstatus(statusinfo)


class getData:
  def GET(self,type,pid):
    try:
      data={"assessmentcount":{},"children":{}}
      cursor = DbManager.getMainCon().cursor()
      if type=="block":
        cursor.execute(statements["block_boundarycounts"],(pid,))
        result = cursor.fetchall()
        for row in result:
          name=row[1]
          id=row[2]
          scount=convertNone(row[3])
          sstucount=convertNone(row[4])
          stucount=convertNone(row[5])
          progname=row[6]
          assessname=row[7]
          smappedcount=convertNone(row[8])
          sassessedcount=convertNone(row[9])
          stuassessedcount=convertNone(row[10])

          if progname !=None and assessname!=None:
            if name in data["assessmentcount"]:
              if progname in data["assessmentcount"][name]:
                data["assessmentcount"][name][progname][assessname]={"smappedcount":smappedcount,"sassessedcount":sassessedcount,"stuassessedcount":stuassessedcount}
              else:
                data["assessmentcount"][name][progname]={assessname:{"smappedcount":smappedcount,"sassessedcount":sassessedcount,"stuassessedcount":stuassessedcount}}
            else:
              data["assessmentcount"][name]={progname:{assessname:{"smappedcount":smappedcount,"sassessedcount":sassessedcount,"stuassessedcount":stuassessedcount}}}
            if name not in data["children"]:
               data["children"][name]={"id":id,"name":name,"scount":scount,"sstucount":sstucount,"stucount":stucount,"assessmentcount":{},"children":{}}
          else:
            if name not in data["children"]:
               data["children"][name]={"id":id,"name":name,"scount":scount,"sstucount":sstucount,"stucount":stucount,"assessmentcount":{},"children":{}}

      elif type=="cluster":
        cursor.execute(statements["cluster_boundarycounts"],(pid,))
        result = cursor.fetchall()
        for row in result:
          district=row[0]
          block=row[1]
          cluster=row[1]
          name=row[2]
          id=row[3]
          scount=convertNone(row[4])
          sstucount=convertNone(row[5])
          stucount=convertNone(row[6])
          progname=row[7]
          assessname=row[8]
          smappedcount=convertNone(row[9])
          sassessedcount=convertNone(row[10])
          stuassessedcount=convertNone(row[11])

          if progname !=None and assessname!=None:
            if name in data["assessmentcount"]:
              if progname in data["assessmentcount"][name]:
                data["assessmentcount"][name][progname][assessname]={"smappedcount":smappedcount,"sassessedcount":sassessedcount,"stuassessedcount":stuassessedcount}
              else:
                data["assessmentcount"][name][progname]={assessname:{"smappedcount":smappedcount,"sassessedcount":sassessedcount,"stuassessedcount":stuassessedcount}}
            else:
              data["assessmentcount"][name]={progname:{assessname:{"smappedcount":smappedcount,"sassessedcount":sassessedcount,"stuassessedcount":stuassessedcount}}}
            if name not in data["children"]:
               data["children"][name]={"id":id,"name":name,"scount":scount,"sstucount":sstucount,"stucount":stucount,"assessmentcount":{},"children":{}}
          else:
            if name not in data["children"]:
               data["children"][name]={"id":id,"name":name,"scount":scount,"sstucount":sstucount,"stucount":stucount,"assessmentcount":{},"children":{}}


      elif type=="school":
        cursor.execute(statements["schoolcounts"],(pid,));
        result = cursor.fetchall()
        for row in result:
          district=row[0]
          block=row[1]
          cluster=row[2]
          name=row[3]
          id=row[4]
          stucount=convertNone(row[5])
          progname=row[6]
          assessname=row[7]
          stuassessedcount=convertNone(row[8])
  
          if progname !=None and assessname!=None:
            if name in data["assessmentcount"]:
              if progname in data["assessmentcount"][name]:
               data["assessmentcount"][name][progname][assessname]={"stuassessedcount":stuassessedcount}
              else:
                data["assessmentcount"][name][progname]={assessname:{"stuassessedcount":stuassessedcount}}
            else:
              data["assessmentcount"][name]={progname:{assessname:{"stuassessedcount":stuassessedcount}}}
            if name not in data["children"]:
               data["children"][name]={"id":id,"name":name,"stucount":stucount,"assessmentcount":{},"children":{}}
          else:
            if name not in data["children"]:
               data["children"][name]={"id":id,"name":name,"stucount":stucount,"assessmentcount":{},"children":{}}


      elif type=="class":
        cursor.execute(statements["classcounts"],(pid,))
        result = cursor.fetchall()
        for row in result:
          data["name"]=row[4]
          district=row[0]
          block=row[1]
          cluster=row[2]
          sid=row[3]
          name=row[4]
          id=row[5]
          stucount=convertNone(row[6])
          progname=row[7]
          assessname=row[8]
          stuassessedcount=convertNone(row[9])
  
          if progname !=None and assessname!=None:
            if name in data["assessmentcount"]:
              if progname in data["assessmentcount"][name]:
               data["assessmentcount"][name][progname][assessname]={"stuassessedcount":stuassessedcount}
               data["children"][name]["assessmentcount"][name][progname][assessname]={"stuassessedcount":stuassessedcount}
              else:
                data["assessmentcount"][name][progname]={assessname:{"stuassessedcount":stuassessedcount}}
                data["children"][name]["assessmentcount"][name][progname]={assessname:{"stuassessedcount":stuassessedcount}}
            else:
              data["assessmentcount"][name]={progname:{assessname:{"stuassessedcount":stuassessedcount}}}
              data["children"][name]={"id":id,"name":name,"stucount":stucount,"assessmentcount":{name:{progname:{assessname:{"stuassessedcount":stuassessedcount}}}},"children":{}}
          else:
            if name not in data["children"]:
               data["children"][name]={"id":id,"name":name,"stucount":stucount,"assessmentcount":{},"children":{}}


      DbManager.getMainCon().commit()
      cursor.close()
    except:
      traceback.print_exc(file=sys.stderr)
      cursor.close()
      DbManager.getMainCon().rollback()


    web.header('Content-Type','application/json')
    return jsonpickle.encode(data)





