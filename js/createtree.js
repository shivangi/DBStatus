//global variable to allow console inspection of tree:
var tree;
var schoolcount={};
var preschoolcount={};
var currentprograms={}
var schooldistrictkeys=[];
var preschooldistrictkeys=[];


function isEmpty(obj) 
{ 
  for(var prop in obj) {
        if(obj.hasOwnProperty(prop))
            return false;
    }

    return true;
} 

function treeInit() 
{
  //instantiate the tree:
  tree = new YAHOO.widget.TreeView("rootnode");
  var schoolNode =new YAHOO.widget.TextNode("schoolcount",tree.getRoot(),false);
  var preschoolNode=new YAHOO.widget.TextNode("preschoolcount",tree.getRoot(),false);
  var currentProgramsNode=new YAHOO.widget.TextNode("currentprograms",tree.getRoot(),false);
  
  createChildNodes(schoolNode,schooldistrictkeys);
  createChildNodes(preschoolNode,preschooldistrictkeys);
  
   // Expand and collapse happen prior to the actual expand/collapse,
   // and can be used to cancel the operation
   tree.subscribe("expand", function(node) 
   {
     YAHOO.log(node.index + " was expanded", "info", "example");
     // return false; // return false to cancel the expand
   });

   tree.subscribe("collapse", function(node) 
   {
     YAHOO.log(node.index + " was collapsed", "info", "example");
   });

   // Trees with TextNodes will fire an event for when the label is clicked:
   tree.subscribe("labelClick", function(node) 
   {
     getdata(node);
     YAHOO.log(node.index + " label was clicked", "info", "example");
   });

   //The tree is not created in the DOM until this method is called:
   tree.draw();
}


function assignData(node,data)
{
  depth=node["depth"];
  if(depth==1)
  {
    root=node["parent"]["label"];
    if(root=="schoolcount")
    {
      schoolcount["children"][node["label"]]["children"]=data["children"];
      schoolcount["children"][node["label"]]["assessmentcount"]=data["assessmentcount"];
      return schoolcount["children"][node["label"]];
    }
    else
    {
      preschoolcount["children"][node["label"]]["children"]=data["children"];
      preschoolcount["children"][node["label"]]["assessmentcount"]=data["assessmentcount"];
      return preschoolcount["children"][node["label"]];
    }
  }
  else if(depth==2)
  {
    //block
    root=node["parent"]["parent"]["label"];
    if(root=="schoolcount")
    {
      schoolcount["children"][node["parent"]["label"]]["children"][node["label"]]["children"]=data["children"];
      schoolcount["children"][node["parent"]["label"]]["children"][node["label"]]["assessmentcount"]=data["assessmentcount"];
      return schoolcount["children"][node["parent"]["label"]]["children"][node["label"]];
    }
    else
    {
      preschoolcount["children"][node["parent"]["label"]]["children"][node["label"]]["children"]=data["children"];
      preschoolcount["children"][node["parent"]["label"]]["children"][node["label"]]["assessmentcount"]=data["assessmentcount"];
      return preschoolcount["children"][node["parent"]["label"]]["children"][node["label"]];
    }
  }
  else if(depth==3)
  {
    //cluster
    root=node["parent"]["parent"]["parent"]["label"];
    district=node["parent"]["parent"]["label"];
    block=node["parent"]["label"];
    if(root=="schoolcount")
    {
      schoolcount["children"][district]["children"][block]["children"][node["label"]]["children"]=data["children"];
      schoolcount["children"][district]["children"][block]["children"][node["label"]]["assessmentcount"]=data["assessmentcount"];
      return schoolcount["children"][district]["children"][block]["children"][node["label"]];
    }
    else
    {
      preschoolcount["children"][district]["children"][block]["children"][node["label"]]["children"]=data["children"];
      preschoolcount["children"][district]["children"][block]["children"][node["label"]]["assessmentcount"]=data["assessmentcount"];
      return preschoolcount["children"][district]["children"][block]["children"][node["label"]];
    }
  }
  else if(depth==4)
  {
    //school
    root=node["parent"]["parent"]["parent"]["parent"]["label"];
    district=node["parent"]["parent"]["parent"]["label"];
    block=node["parent"]["parent"]["label"];
    cluster=node["parent"]["label"];
    if(root=="schoolcount")
    {
      schoolcount["children"][district]["children"][block]["children"][cluster]["children"][node["label"]]["children"]=data["children"]
      schoolcount["children"][district]["children"][block]["children"][cluster]["children"][node["label"]]["assessmentcount"]=data["assessmentcount"]
      return schoolcount["children"][district]["children"][block]["children"][cluster]["children"][node["label"]];
    }
    else
    {
      preschoolcount["children"][district]["children"][block]["children"][cluster]["children"][node["label"]]["children"]=data["children"]
      preschoolcount["children"][district]["children"][block]["children"][cluster]["children"][node["label"]]["assessmentcount"]=data["assessmentcount"]
      return preschoolcount["children"][district]["children"][block]["children"][cluster]["children"][node["label"]];
    }
  }
}

function getdata(node)
{
  if(node["label"]=="currentprograms")
  {
    var content="<div class='div-table'><div class='div-table-caption' >Current Programs</div>";
    for(num in currentprograms)
    {
      program=currentprograms[num];
      content=content+"<div class='div-table-row'><div class='div-table-col'  style='width:220px'>"+program+"</div></div>";
    }
    content=content+"</div>"
    document.getElementById("load_data").innerHTML=content;
    return;
  }

  depth=node["depth"];
  if(depth==0)
  {
     //its the root
    root=node["label"];
    var data;
    if(root=="schoolcount")
      data=schoolcount;
    else
      data=preschoolcount;

    var content="";
    showBoundaryData(content,data,depth);
  }
  else if(depth==1)
  {
    //district
    root=node["parent"]["label"];
    var data;
    if(root=="schoolcount")
      data=schoolcount["children"][node["label"]]
    else
      data=preschoolcount["children"][node["label"]]

    var content="<div><p>"+data["name"]+" ("+data["id"]+")</p></div>";
    if( isEmpty(data["children"]))
    {
      getChildData("block",data["id"],node,content,data,depth);
      document.getElementById("load_data").innerHTML="Loading...";
    }
    else
      showBoundaryData(content,data,depth); 
  }
  else if(depth==2)
  {
    //block
    root=node["parent"]["parent"]["label"];
    if(root=="schoolcount")
    {
      data=schoolcount["children"][node["parent"]["label"]]["children"][node["label"]];
      datacount=schoolcount["children"];
    }
    else
    {
      data=preschoolcount["children"][node["parent"]["label"]]["children"][node["label"]];
      datacount=preschoolcount["children"];

    }

    var content="<div><p>"+datacount[node["parent"]["label"]]["name"]+"->"+data["name"]+"("+data["id"]+")</p></div>";
    if( isEmpty(data["children"]))
    {
      getChildData("cluster",data["id"],node,content,data,depth);
      document.getElementById("load_data").innerHTML="Loading...";
    }
    else
      showBoundaryData(content,data,depth); 

  }
  else if(depth==3)
  {
    //cluster
    root=node["parent"]["parent"]["parent"]["label"];
    district=node["parent"]["parent"]["label"];
    block=node["parent"]["label"];
    if(root=="schoolcount")
    {
      datacount=schoolcount["children"];
      data=schoolcount["children"][district]["children"][block]["children"][node["label"]];
    }
    else
    {
      datacount=preschoolcount["children"];
      data=preschoolcount["children"][district]["children"][block]["children"][node["label"]];
    }

    var content="<div><p>"+datacount[district]["name"]+"->"+datacount[district]["children"][block]["name"]+"->"+data["name"]+"("+data["id"]+")</p></div>";
    if( isEmpty(data["children"]))
    {
      getChildData("school",data["id"],node,content,data,depth);
      document.getElementById("load_data").innerHTML="Loading...";
    }
    else
      showBoundaryData(content,data,depth); 

  }
  else if(depth==4)
  {
    //school
    root=node["parent"]["parent"]["parent"]["parent"]["label"];
    district=node["parent"]["parent"]["parent"]["label"];
    block=node["parent"]["parent"]["label"];
    cluster=node["parent"]["label"];
    if(root=="schoolcount")
    {
      data=schoolcount["children"][district]["children"][block]["children"][cluster]["children"][node["label"]];
      datacount=schoolcount["children"];
    }
    else
    {
      data=preschoolcount["children"][district]["children"][block]["children"][cluster]["children"][node["label"]];
      datacount=preschoolcount["children"];
    }

    var content="<div><p>"+datacount[district]["name"]+"->"+datacount[district]["children"][block]["name"]+"->"+datacount[district]["children"][block]["children"][cluster]["name"]+"->"+data["name"]+"("+data["id"]+")</p></div>";
    if( isEmpty(data["children"]))
    {
      getChildData("class",data["id"],node,content,data,depth);
      document.getElementById("load_data").innerHTML="Loading...";
    }
    else
      showSchoolData(content,data); 
  }
  else if(depth==5)
  {
    //class
    root=node["parent"]["parent"]["parent"]["parent"]["parent"]["label"];
    district=node["parent"]["parent"]["parent"]["parent"]["label"];
    block=node["parent"]["parent"]["parent"]["label"];
    cluster=node["parent"]["parent"]["label"];
    school=node["parent"]["label"];
    if(root=="schoolcount")
    {
      data=schoolcount["children"][district]["children"][block]["children"][cluster]["children"][school]["children"][node["label"]];
      datacount=schoolcount["children"];
    }
    else
    {
      data=preschoolcount["children"][district]["children"][block]["children"][cluster]["children"][school]["children"][node["label"]];
      datacount=preschoolcount["children"];
    }

    var content="<div><p>"+datacount[district]["name"]+"->"+datacount[district]["children"][block]["name"]+"->"+datacount[district]["children"][block]["children"][cluster]["name"]+"->"+datacount[district]["children"][block]["children"][cluster]["children"][school]["name"]+"->"+data["name"]+"("+data["id"]+")</p></div>"; 
  
    showSchoolData(content,data); 
  }
}


function getChildData(type,id,node,content,data,depth)
{
    YUI({base: 'yui3/build/',
    timeout: 50000}).use("io-base","json-parse",
    function(Y, result) {
      if (!result.success) {
        Y.log('Load failure: ' + result.msg, 'warn', 'program');
      }
      var callback = {
        on: { success:
          function(id, o) {
            try {
              var retdata= Y.JSON.parse(o.responseText);
            } catch (e) {
              Y.log('Could not parse json', 'error', 'retdata');
              return ;
            }
            bkeys=keys(retdata["children"]).sort();
            data=assignData(node,retdata);
            createChildNodes(node,bkeys);
            tree.draw();
            if (type=="class")
            {
              showSchoolData(content,data); 
            }
            else
            {
              showBoundaryData(content,data,depth); 
            }
          },
          failure: function(id, o) {
            Y.log('Could not retrieve data ','error','data');
          }
        }
      };
      url = "getdata/"+type+"/"+id
      var request = Y.io(url, callback);
    });

}

function showBoundaryData(incontent,data,depth)
{
    var content=incontent+"<div class='div-table'><div class='div-table-caption' >Counts</div><div class='div-table-row'><div class='div-table-col' style='width:200px'>Active School Count</div><div class='div-table-col' style='width:200px'>"+data["scount"]+"</div></div><div class='div-table-row'><div class='div-table-col' style='width:200px'>Active School with Students Count</div><div class='div-table-col' style='width:200px'>"+data["sstucount"]+"</div></div><div class='div-table-row'><div class='div-table-col' style='width:200px'>Active Students Count</div><div class='div-table-col' style='width:200px'>"+data["stucount"]+"</div></div></div>";
    content=content+"<br><br>";
    if( depth !==3 )
    {
      content=content+"<div class='div-table'><div class='div-table-caption'>Assessment Counts</div><div  class='div-table-row'><div class='div-table-col'>Boundary</div><div class='div-table-col'>Program Name</div><div class='div-table-col'>Assess Name</div><div class='div-table-col'>Schools Mapped</div><div class='div-table-col'>Schools Assessed</div><div class='div-table-col'>Student Assessed</div></div>";
      var asscount=0;
      var bkeys=keys(data["assessmentcount"]).sort();
      for (bkey in bkeys)
      {
        var bname=bkeys[bkey];
        var pkeys=keys(data["assessmentcount"][bname]).sort();
        for (pkey in pkeys)
        {
          var pname=pkeys[pkey];
          var asskeys=keys(data["assessmentcount"][bname][pname]).sort();
          for (akey in asskeys)
          {
             var assname=asskeys[akey];
             asscount=asscount+1;
             content=content+"<div class='div-table-row'><div class='div-table-col'>"+bname+"</div><div class='div-table-col'>"+pname+"</div><div class='div-table-col'>"+assname+"</div><div class='div-table-col'>"+data["assessmentcount"][bname][pname][assname]["smappedcount"]+"</div><div class='div-table-col'>"+data["assessmentcount"][bname][pname][assname]["sassessedcount"]+"</div><div class='div-table-col'>"+data["assessmentcount"][bname][pname][assname]["stuassessedcount"]+"</div></div>";
          }
        }  
      }  
      if(asscount==0)
      {
        content=content+"<div  class='div-table-row'><div class='div-table-col'>-</div><div class='div-table-col'>-</div><div class='div-table-col'>-</div><div class='div-table-col'>-</div><div class='div-table-col'>-</div><div class='div-table-col'>-</div></div>";
      }
    }
    else
    {
      content=content+"<div class='div-table'><div class='div-table-caption'>Assessment Counts</div><div  class='div-table-row'><div class='div-table-col' style='width:100px'>Boundary</div><div class='div-table-col' style='width:100px'>Program Name</div><div class='div-table-col' style='width:100px'>Assessment Name</div><div class='div-table-col' style='width:100px'>Student Assessed</div></div>";
      var asscount=0;
      var bkeys=keys(data["assessmentcount"]).sort();
      for (bkey in bkeys)
      {
        var bname=bkeys[bkey];
        var pkeys=keys(data["assessmentcount"][bname]).sort();
        for (pkey in pkeys)
        {
          var pname=pkeys[pkey];
          var asskeys=keys(data["assessmentcount"][bname][pname]).sort();
          for (akey in asskeys)
          {
             var assname=asskeys[akey];
             asscount=asscount+1;
             content=content+"<div class='div-table-row'><div class='div-table-col' style='width:100px'>"+bname+"</div><div class='div-table-col' style='width:100px'>"+pname+"</div><div class='div-table-col' style='width:100px'>"+assname+"</div><div class='div-table-col' style='width:100px'>"+data["assessmentcount"][bname][pname][assname]["stuassessedcount"]+"</div></div>";
          }
        }  
      }  
      if(asscount==0)
      {
        content=content+"<div  class='div-table-row'><div class='div-table-col' style='width:100px' >-</div><div class='div-table-col' style='width:100px'>-</div><div class='div-table-col' style='width:100px'>-</div><div class='div-table-col' style='width:100px'>-</div></div>";
      }
    
    }
    content=content+"</div>";
      
    document.getElementById("load_data").innerHTML=content;
}


function showSchoolData(incontent,data)
{
  var content=incontent+"<div class='div-table'><div class='div-table-caption' >Counts</div><div class='div-table-row'><div class='div-table-col' style='width:200px'>Active Students Count</div><div class='div-table-col' style='width:200px'>"+data["stucount"]+"</div></div></div>";
    content=content+"<br><br>";
    content=content+"<div class='div-table'><div class='div-table-caption'>Assessment Counts</div><div  class='div-table-row'><div class='div-table-col' style='width:100px'>Program Name</div><div class='div-table-col' style='width:100px'>Assessment Name</div><div class='div-table-col' style='width:100px'>Student Assessed</div></div>";
    var asscount=0;
    var bkeys=keys(data["assessmentcount"]).sort();
    for (bkey in bkeys)
    {
      var bname=bkeys[bkey];
      var pkeys=keys(data["assessmentcount"][bname]).sort();
      for (pkey in pkeys)
      {
        var pname=pkeys[pkey];
        var asskeys=keys(data["assessmentcount"][bname][pname]).sort();
        for (akey in asskeys)
        {
           var assname=asskeys[akey];
           asscount=asscount+1;
           content=content+"<div class='div-table-row'><div class='div-table-col' style='width:100px' >"+pname+"</div><div class='div-table-col'  style='width:100px'>"+assname+"</div><div class='div-table-col' style='width:100px'>"+data["assessmentcount"][bname][pname][assname]["stuassessedcount"]+"</div></div>";
        }
      }
    }
    if(asscount==0)
    {
      content=content+"<div  class='div-table-row'><div class='div-table-col' style='width:100px'>-</div><div class='div-table-col' style='width:100px'>-</div><div class='div-table-col' style='width:100px'>-</div></div>";
    }
    content=content+"</div>";
    document.getElementById("load_data").innerHTML=content;
}
 


function createChildNodes(treenode,datakeys)
{
  for (key in datakeys)
  {
     var treelabel=datakeys[key];
     var treeNode= new YAHOO.widget.TextNode(treelabel, treenode, true);
  }
}


function keys(obj)
{
    var keys = [];

    for(var key in obj)
    {
        if(obj.hasOwnProperty(key))     
        {
            keys.push(key);
        }
    }

    return keys;
}


function loadinitialContent()
{
    var content="<h2>School Counts</h2>";
    data=schoolcount;
    showBoundaryData(content,data,0);
    content=document.getElementById("load_data").innerHTML;
    content= content+"<br><br><h2>Preschool Counts</h2>";
    data=preschoolcount;
    showBoundaryData(content,data,0);
}

function createTree(statusinfo)
{
  schoolcount=statusinfo["schoolcount"];
  schooldistrictkeys=keys(statusinfo["schoolcount"]["children"]).sort();
  preschoolcount=statusinfo["preschoolcount"];
  preschooldistrictkeys=keys(statusinfo["preschoolcount"]["children"]).sort();
  currentprograms=statusinfo["currentprograms"];
  document.getElementById("heading").innerHTML="<h1>Akshara DB Counts </h1>   (Last updated at:"+statusinfo["updatedtime"]+")<br>";
  loadinitialContent();

  YAHOO.util.Event.onDOMReady(treeInit);
}
