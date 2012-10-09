#!/usr/bin/env python
import os,sys
import psycopg2
import Utility.KLPDB



connection = Utility.KLPDB.getklpConnection()
cursor = connection.cursor()


queries={'tb_boundary_schoolcount':['select b2.id, count(distinct s.id) from schools_boundary b,schools_boundary b1,schools_boundary b2,schools_institution s where s.boundary_id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and s.active=2 group by b2.id',
'select b1.id , count(distinct s.id) from schools_boundary b,schools_boundary b1,schools_boundary b2,schools_institution s where s.boundary_id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and s.active=2 group by b1.id',
'select b.id, count(distinct s.id) from schools_boundary b,schools_boundary b1,schools_boundary b2,schools_institution s where s.boundary_id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and s.active=2 group by b.id'],
'tb_boundary_studentcount':['select b2.id,count(distinct s.id),count(distinct stu.id) from schools_student_studentgrouprelation stusg,schools_studentgroup sg,schools_student stu,schools_institution s,schools_boundary b,schools_boundary b1,schools_boundary b2 where s.boundary_id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and s.active=2 and sg.institution_id=s.id and sg.active=2 and stusg.student_group_id=sg.id and stusg.active=2 and stusg.academic_id=121 and stusg.student_id=stu.id and stu.active=2 group by b2.id',
'select b1.id,count(distinct s.id),count(distinct stu.id) from schools_student_studentgrouprelation stusg,schools_studentgroup sg,schools_student stu,schools_institution s,schools_boundary b,schools_boundary b1,schools_boundary b2 where s.boundary_id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and s.active=2 and sg.institution_id=s.id and sg.active=2 and stusg.student_group_id=sg.id and stusg.active=2 and stusg.academic_id=121 and stusg.student_id=stu.id and stu.active=2 group by b1.id',
'select b.id,count(distinct s.id),count(distinct stu.id) from schools_student_studentgrouprelation stusg,schools_studentgroup sg,schools_student stu,schools_institution s,schools_boundary b,schools_boundary b1,schools_boundary b2 where s.boundary_id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and s.active=2 and sg.institution_id=s.id and sg.active=2 and stusg.student_group_id=sg.id and stusg.active=2 and stusg.academic_id=121 and stusg.student_id=stu.id and stu.active=2 group by b.id'],
'tb_boundary_assessmentcount':['select distinct schoolsmapped.b2id,schoolsmapped.pname,schoolsmapped.assname,schoolsmapped.countmapped,schoolsassessed.countassessed,schoolsassessed.countstuassessed from (select distinct b2.id as b2id ,p.name as pname,ass.name as assname,count(distinct s.id) as countmapped from schools_assessment ass,schools_programme p,schools_studentgroup sg,schools_institution s,schools_boundary b,schools_boundary b1,schools_boundary b2,schools_assessment_studentgroup_association sgass where sgass.student_group_id=sg.id and sgass.assessment_id=ass.id and sg.active=2 and sg.institution_id=s.id and s.boundary_id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and  ass.programme_id=p.id and p.active=2 group by b2.id,p.name,ass.name)schoolsmapped left outer join ( select distinct b2.id as b2id,p.name as pname,ass.name as assname,count(distinct s.id) as countassessed, count(distinct stu.id) as countstuassessed from schools_answer se,schools_question q,schools_assessment ass,schools_programme p,schools_student_studentgrouprelation stusg,schools_studentgroup sg,schools_student stu,schools_institution s,schools_boundary b,schools_boundary b1,schools_boundary b2 where se.object_id=stu.id and stusg.student_id=stu.id and stusg.active=2 and stusg.academic_id=121 and stusg.student_group_id=sg.id and sg.active=2 and sg.institution_id=s.id and s.boundary_id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and se.question_id=q.id and q.assessment_id=ass.id and ass.programme_id=p.id and p.active=2 group by b2.id,p.name,ass.name)schoolsassessed on (schoolsmapped.b2id=schoolsassessed.b2id  and  schoolsmapped.pname=schoolsassessed.pname and schoolsmapped.assname=schoolsassessed.assname)',
'select distinct schoolsmapped.b1id,schoolsmapped.pname,schoolsmapped.assname,schoolsmapped.countmapped,schoolsassessed.countassessed,schoolsassessed.countstuassessed from (select distinct b1.id as b1id ,p.name as pname,ass.name as assname,count(distinct s.id) as countmapped from schools_assessment ass,schools_programme p,schools_studentgroup sg,schools_institution s,schools_boundary b,schools_boundary b1,schools_boundary b2,schools_assessment_studentgroup_association sgass where sgass.student_group_id=sg.id and sgass.assessment_id=ass.id and sg.active=2 and sg.institution_id=s.id and s.boundary_id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and  ass.programme_id=p.id and p.active=2 group by b1.id,p.name,ass.name)schoolsmapped left outer join ( select distinct b1.id as b1id,p.name as pname,ass.name as assname,count(distinct s.id) as countassessed, count(distinct stu.id) as countstuassessed from schools_answer se,schools_question q,schools_assessment ass,schools_programme p,schools_student_studentgrouprelation stusg,schools_studentgroup sg,schools_student stu,schools_institution s,schools_boundary b,schools_boundary b1,schools_boundary b2 where se.object_id=stu.id and stusg.student_id=stu.id and stusg.active=2 and stusg.academic_id=121 and stusg.student_group_id=sg.id and sg.active=2 and sg.institution_id=s.id and s.boundary_id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and se.question_id=q.id and q.assessment_id=ass.id and ass.programme_id=p.id and p.active=2 group by b1.id,p.name,ass.name)schoolsassessed on (schoolsmapped.b1id=schoolsassessed.b1id  and  schoolsmapped.pname=schoolsassessed.pname and schoolsmapped.assname=schoolsassessed.assname)',
'select distinct schoolsmapped.bid,schoolsmapped.pname,schoolsmapped.assname,schoolsmapped.countmapped,schoolsassessed.countassessed,schoolsassessed.countstuassessed from (select distinct b.id as bid ,p.name as pname,ass.name as assname,count(distinct s.id) as countmapped from schools_assessment ass,schools_programme p,schools_studentgroup sg,schools_institution s,schools_boundary b,schools_boundary b1,schools_boundary b2,schools_assessment_studentgroup_association sgass where sgass.student_group_id=sg.id and sgass.assessment_id=ass.id and sg.active=2 and sg.institution_id=s.id and s.boundary_id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and  ass.programme_id=p.id and p.active=2 group by b.id,p.name,ass.name)schoolsmapped left outer join ( select distinct b.id as bid,p.name as pname,ass.name as assname,count(distinct s.id) as countassessed, count(distinct stu.id) as countstuassessed from schools_answer se,schools_question q,schools_assessment ass,schools_programme p,schools_student_studentgrouprelation stusg,schools_studentgroup sg,schools_student stu,schools_institution s,schools_boundary b,schools_boundary b1,schools_boundary b2 where se.object_id=stu.id and stusg.student_id=stu.id and stusg.active=2 and stusg.academic_id=121 and stusg.student_group_id=sg.id and sg.active=2 and sg.institution_id=s.id and s.boundary_id=b.id and b.parent_id=b1.id and b1.parent_id=b2.id and se.question_id=q.id and q.assessment_id=ass.id and ass.programme_id=p.id and p.active=2 group by b.id,p.name,ass.name)schoolsassessed on (schoolsmapped.bid=schoolsassessed.bid  and  schoolsmapped.pname=schoolsassessed.pname and schoolsmapped.assname=schoolsassessed.assname)'],
'tb_currentprograms':['select name from schools_programme where active=2'],
'tb_schoolstudentcount':['select distinct s.id,count(distinct stu.id) from schools_student_studentgrouprelation stusg,schools_studentgroup sg,schools_institution s,schools_student stu where stusg.student_id=stu.id and stu.active=2 and stusg.academic_id=121 and stusg.active=2 and stusg.student_group_id=sg.id and sg.active=2 and sg.institution_id=s.id and s.active=2 group by s.id'],
'tb_classstudentcount':["select distinct sg.id,s.id,sg.name,sg.section,count(distinct stu.id) from schools_student_studentgrouprelation stusg,schools_studentgroup sg,schools_institution s,schools_student stu where stusg.student_id=stu.id and stu.active=2 and stusg.academic_id=121 and stusg.active=2 and stusg.student_group_id=sg.id and sg.active=2 and sg.group_type='Class' and sg.institution_id=s.id and s.active=2 group by sg.id,s.id,sg.name,sg.section"],
'tb_schoolassessmentcount':['select distinct s.id,p.name,ass.name,count(distinct stu.id) from schools_answer se,schools_student_studentgrouprelation stusg,schools_studentgroup sg,schools_institution s,schools_student stu,schools_question q,schools_assessment ass,schools_programme p where se.object_id=stu.id and stu.active=2 and stu.id=stusg.student_id and stusg.academic_id=121 and stusg.active=2 and stusg.student_group_id=sg.id and sg.active=2 and sg.institution_id=s.id and s.active=2 and se.question_id=q.id and q.assessment_id=ass.id and ass.programme_id=p.id and p.active=2 group by s.id,p.name,ass.name'],
'tb_classassessmentcount':["select distinct sg.id,s.id,sg.name,sg.section,p.name,ass.name,count(distinct stu.id) from schools_answer se,schools_student_studentgrouprelation stusg,schools_studentgroup sg,schools_institution s,schools_student stu,schools_question q,schools_assessment ass,schools_programme p where se.object_id=stu.id and stu.active=2 and stu.id=stusg.student_id and stusg.academic_id=121 and stusg.active=2 and stusg.student_group_id=sg.id and sg.active=2 and sg.group_type='Class' and sg.institution_id=s.id and s.active=2 and se.question_id=q.id and q.assessment_id=ass.id and ass.programme_id=p.id and p.active=2 group by sg.id,s.id,sg.name,sg.section,p.name,ass.name"]
}

rootdir=os.path.dirname(sys.argv[0])
loadfile=open(rootdir+'/load/load.sql','w',0)

def getRow(row):
  line=str(row).strip('(')
  line = line.strip(')')
  line = line.strip()
  line = line.replace('\'','"')
  line = line.replace('None','')
  return line


def getDataName(cursor,file):
   for row in cursor:
    firstdata=1
    datacount=0
    name=""
    namecheck=0
    for data in row:
      datacount=datacount+1
      data=str(data)
      print data+" "+str(datacount)+" "+str(namecheck)
      if datacount==2:
        namecheck=1
        if data=='None':
          data=''
        name=data
      if datacount==3:
        namecheck=1
        if data=='None':
          data=''
        else:
          name=name+" "+data
      if datacount==4:
        if data=='None':
          data=''
        else:
          name=name+" "+data
        data=name
        namecheck=0
      print namecheck
      if namecheck:
         continue  
      if firstdata:
        if data=="":
          file.write(data)
        elif data=='None':
          file.write('')
        else:
          file.write('"'+data+'"')
        firstdata=0
      else:
        if data=="":
          file.write(","+data)
        elif data=="None":
          file.write(',')
        else:
          file.write(',"'+data+'"')
    file.write("\n")


def createboundaryassessmentdata(query,tbname):
  cursor.execute(queries[query])
  boundarycount={0:{},1:{}}
  for row in cursor:
    print row
    district=row[0]
    block=row[1]
    pname=row[3]
    assname=row[4]
    smapped=row[5]
    sassessed=row[6]
    stuassessed=row[7]
    if stuassessed==None:
      stuassessed=0
    if sassessed==None:
      sassessed=0
    print sassessed
    print smapped
    print stuassessed
    if district in boundarycount[0]:
      if pname in boundarycount[0][district]:
        if assname in boundarycount[0][district][pname]:
          print boundarycount[0][district][pname][assname]
          boundarycount[0][district][pname][assname]["sassessed"]=boundarycount[0][district][pname][assname]["sassessed"]+sassessed
          boundarycount[0][district][pname][assname]["smapped"]=boundarycount[0][district][pname][assname]["smapped"]+smapped
          boundarycount[0][district][pname][assname]["stuassessed"]=boundarycount[0][district][pname][assname]["stuassessed"]+stuassessed
        else:
          boundarycount[0][district][pname][assname]={"sassessed":sassessed,"smapped":smapped,"stuassessed":stuassessed}
      else:
          boundarycount[0][district][pname]={assname:{"sassessed":sassessed,"smapped":smapped,"stuassessed":stuassessed}}
    else:
      boundarycount[0][district]={pname:{assname:{"sassessed":sassessed,"smapped":smapped,"stuassessed":stuassessed}}}

    if block in boundarycount[1]:
      if pname in boundarycount[1][block]:
        if assname in boundarycount[1][block][pname]:
          boundarycount[1][block][pname][assname]["sassessed"]=boundarycount[1][block][pname][assname]["sassessed"]+sassessed
          boundarycount[1][block][pname][assname]["smapped"]=boundarycount[1][block][pname][assname]["smapped"]+smapped
          boundarycount[1][block][pname][assname]["stuassessed"]=boundarycount[1][block][pname][assname]["stuassessed"]+stuassessed
        else:
          boundarycount[1][block][pname][assname]={"sassessed":sassessed,"smapped":smapped,"stuassessed":stuassessed}
      else:
          boundarycount[1][block][pname]={assname:{"sassessed":sassessed,"smapped":smapped,"stuassessed":stuassessed}}
    else:
      boundarycount[1][block]={pname:{assname:{"sassessed":sassessed,"smapped":smapped,"stuassessed":stuassessed}}}
     
  filename=rootdir+'/load/'+tbname+'.csv'
  loadfile.write("copy "+tbname+" from '"+filename+"' with csv;\n")
  file=open(filename,'w',0)
  for boundary in boundarycount[0]:
    for pname in boundarycount[0][boundary]:
      for assname in boundarycount[0][boundary][pname]:
        file.write('"'+boundary+'","0","'+pname+'","'+assname+'","'+str(boundarycount[0][boundary][pname][assname]["smapped"])+'","'+str(boundarycount[0][boundary][pname][assname]["sassessed"])+'","'+str(boundarycount[0][boundary][pname][assname]["stuassessed"])+'"\n')
    
  for boundary in boundarycount[1]:
    for pname in boundarycount[1][boundary]:
      for assname in boundarycount[1][boundary][pname]:
        file.write('"'+boundary+'","1","'+pname+'","'+assname+'","'+str(boundarycount[1][boundary][pname][assname]["smapped"])+'","'+str(boundarycount[1][boundary][pname][assname]["sassessed"])+'","'+str(boundarycount[1][boundary][pname][assname]["stuassessed"])+'"\n')
    

def createboundarystudentdata(query,tbname):
  cursor.execute(queries[query])
  boundarycount={0:{},1:{}}
  for row in cursor:
    if row[0] in boundarycount[0]:
      boundarycount[0][row[0]]["schoolcount"]=boundarycount[0][row[0]]["schoolcount"]+row[3]
      boundarycount[0][row[0]]["studentcount"]=boundarycount[0][row[0]]["studentcount"]+row[4]
    else:
      boundarycount[0][row[0]]={"schoolcount":row[3],"studentcount":row[4]}
    if row[1] in boundarycount[1]:
      boundarycount[1][row[1]]["schoolcount"]=boundarycount[1][row[1]]["schoolcount"]+row[3]
      boundarycount[1][row[1]]["studentcount"]=boundarycount[1][row[1]]["studentcount"]+row[4]
    else:
      boundarycount[1][row[1]]={"schoolcount":row[3],"studentcount":row[4]}
  filename=rootdir+'/load/'+tbname+'.csv'
  loadfile.write("copy "+tbname+" from '"+filename+"' with csv;\n")
  file=open(filename,'w',0)
  for boundary in boundarycount[0]:
    file.write('"'+boundary+'","0","'+str(boundarycount[0][boundary]["schoolcount"])+'","'+str(boundarycount[0][boundary]["studentcount"])+'"\n')
  for boundary in boundarycount[1]:
    file.write('"'+boundary+'","1","'+str(boundarycount[1][boundary]["schoolcount"])+'","'+str(boundarycount[1][boundary]["studentcount"])+'"\n')
    



def createboundarydata(query,tbname):
  cursor.execute(queries[query])
  boundarycount={0:{},1:{}}
  for row in cursor:
    if row[0] in boundarycount[0]:
      boundarycount[0][row[0]]=boundarycount[0][row[0]]+row[3]
    else:
      boundarycount[0][row[0]]=row[3]
    if row[1] in boundarycount[1]:
      boundarycount[1][row[1]]=boundarycount[1][row[1]]+row[3]
    else:
      boundarycount[1][row[1]]=row[3]
  filename=rootdir+'/load/'+tbname+'.csv'
  loadfile.write("copy "+tbname+" from '"+filename+"' with csv;\n")
  file=open(filename,'w',0)
  for boundary in boundarycount[0]:
    file.write('"'+boundary+'","0","'+str(boundarycount[0][boundary])+'"\n')
  for boundary in boundarycount[1]:
    file.write('"'+boundary+'","1","'+str(boundarycount[1][boundary])+'"\n')
    


def write_csv(query,file):
  print "Executing qurey"
  sys.stdout.flush()
  cursor.execute(query)
  print "Finished executing query"
  sys.stdout.flush()
  for row in cursor:
    firstdata=1
    for data in row:
      data=str(data)
      if firstdata:
        if data=="":
          file.write(data)
        elif data=='None':
          file.write('')
        else:
          file.write('"'+data+'"')
        firstdata=0
      else:
        if data=="":
          file.write(","+data)
        elif data=="None":
          file.write(',')
        else:
          file.write(',"'+data+'"')
    file.write("\n")
  

for tbname in queries:
  print tbname
  filename=rootdir+'/load/'+tbname+'.csv'
  loadfile.write("copy "+tbname+" from '"+filename+"' with csv;\n")
  file=open(filename,'w',0)
  for query in queries[tbname]:
    write_csv(query,file)

connection.close()
