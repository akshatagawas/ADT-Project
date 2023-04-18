// ADD NEW BOARD FEATURE

function Show_board(){
  var x ;
  
  x=document.getElementById("create-new-board").style.display="flex";
  x=document.getElementById("overlay1").style.display="block";
}
function HideBoard(){
var y ;

y=document.getElementById("create-new-board").style.display="none";
y=document.getElementById("overlay1").style.display="none";

}
function editBoard(){
var y;
y=document.getElementById('board-name').value = '';

}




function pushBoard(){
  var new_field=[];
     // get value from the input text
     var board_name= document.getElementById('board-name').value;
     new_field.push(board_name);
     
     if(board_name.localeCompare("")!=0)
    { for(i = 0; i < new_field.length; i++)
      { const el = document.createElement('li');
      el.setAttribute("disabled", "");
      el.textContent=new_field[i];
     
      var tasklists=document.getElementById("tasklist");
      var names=document.getElementById("board-name").value;
      tasklists.innerHTML += `<li draggable="true" tabindex="1" ondragstart="drag(event)" id="${names.toLowerCase().split(" ").join("")}"><img src="images/tasklogo.jpg" alt="" class="tasklogo">${names}</li>`
      editBoard();
      HideBoard();
      }

    }
}

/*------------------------------ */

// CREATE NEW TASK POPUP

function Show(){
    var x ;
    
    x=document.getElementById("create-new-task-block").style.display="flex";
    x=document.getElementById("overlay").style.display="block";
}

function Hide(){
    var x;
         x=document.getElementById('task-name').value = '';
         x=document.getElementById('task-description').value = '';
         x=document.getElementById('task-status').value = '';
    var y ;
    
    y=document.getElementById("create-new-task-block").style.display="none";
    y=document.getElementById("overlay").style.display="none";
}

/*------------------------------ */

// DELETING TASK
function delete_task(el){
   
    var childId = document.getElementById(el); 
	
        childId.parentNode.removeChild(childId);
      }

/*------------------------------ */   

// EDIT DROPDOWN

function openmenu(){
    var z;

    z=document.getElementById("myDropdown").style.display="flex";
    
}

function closemenu(){
    var m;

    m=document.getElementById("myDropdown").style.display="none";
}

/*------------------------------ */ 

// DRAG FEATURE

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}


function allowDrop(ev) {
    ev.preventDefault();
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.currentTarget.appendChild(document.getElementById(data));
}
function pushData()
 {
    var new_field=[];
     // get value from the input text
     var status_option = document.getElementById('task-status').value;
     var task_name = document.getElementById('task-name').value;
     // append data to the array
     new_field.push(task_name);
     
     if((task_name.localeCompare("")!=0)&&(status_option.localeCompare("")!=0))
    {for(i = 0; i < new_field.length; i++)
     {
         
         const el = document.createElement('div');
         el.setAttribute("class","task");
         el.setAttribute("disabled", "");

         el.textContent = new_field[i];
         if(status_option.localeCompare("todo")==0)
         {
            var todo = document.getElementById("todo");
            var taskName = document.getElementById("task-name").value;
            todo.innerHTML += `<div class="task" id="${taskName.toLowerCase().split(" ").join("")}" draggable="true" ondragstart="drag(event)">
                <span>${taskName}</span>
                <img src="images/closebutton.png" class="closebutton2" id="${taskName.toLowerCase().split(" ").join("")}" onclick="delete_task(this.id)">
            </div>
            `
             
         }
         else if(status_option.localeCompare("inprogress")==0)
         {
            var inprogress = document.getElementById("inprogress");
            var taskName = document.getElementById("task-name").value;
            inprogress.innerHTML += `<div class="task" id="${taskName.toLowerCase().split(" ").join("")}" draggable="true" ondragstart="drag(event)">
                <span>${taskName}</span>
                <img src="images/closebutton.png" class="closebutton2" id="${taskName.toLowerCase().split(" ").join("")}" onclick="delete_task(this.id)">
            </div>
            `
         }
         else
         {
            var done = document.getElementById("done");
            var taskName = document.getElementById("task-name").value;
            done.innerHTML += `<div class="task" id="${taskName.toLowerCase().split(" ").join("")}" draggable="true" ondragstart="drag(event)">
                <span>${taskName}</span>
                <img src="images/closebutton.png" class="closebutton2" id="${taskName.toLowerCase().split(" ").join("")}" onclick="delete_task(this.id)">
            </div>
            `
         }
         var x;
         x=document.getElementById('task-name').value = '';
         x=document.getElementById('task-description').value = '';
         x=document.getElementById('task-status').value = '';
              
         
         var y ;
    
    y=document.getElementById("create-new-task-block").style.display="none";
    y=document.getElementById("overlay").style.display="none";
        
    }
    
    }
   
} 
function editTask(){
  var y;
  y=document.getElementById('task-name').value = '';
  y=document.getElementById('task-description').value = '';
  y=document.getElementById('task-status').value = '';
  
}

/*------------------------------ */


// Changing name of the board

function openchangetitle(){
    var x ;
    
    x=document.getElementById("changename").style.display="flex";
    x=document.getElementById("overlay2").style.display="block";
}

function closechangetitle(){
    var x ;
    
    x=document.getElementById("changename").style.display="none";
    
}

const txt1= document.getElementById('changetitle');

const title1= document.getElementById('task_title');

function newchange(){
  title1.innerHTML=txt1.value;
  var x ;
  x=document.getElementById("changename").style.display="none";
  x=document.getElementById("myDropdown").style.display="none";
}  

/*------------------------------ */



// DARK MODE TOGGLE

var t=0;
function darkmode() {
 t=t+1;
  if(t%2!=0)
  {x=document.getElementById('box').style.backgroundColor = 'black';
  x=document.getElementById('top_panel').style.backgroundColor = 'black';
  x=document.getElementById('leftpanel').style.backgroundColor = 'black';
}
else{
  x=document.getElementById('box').style.backgroundColor = '#ffffff';
  x=document.getElementById('top_panel').style.backgroundColor = '#ed9fd9';
  x=document.getElementById('leftpanel').style.backgroundColor = '#8bd7a2';
}

function lightmode() {
  t = t + 1;
  if (t % 2 != 0) {
    x = document.getElementById('box').style.backgroundColor = 'white';
    x = document.getElementById('top_panel').style.backgroundColor = 'white';
    x = document.getElementById('leftpanel').style.backgroundColor = 'white';
  } else {
    x = document.getElementById('box').style.backgroundColor = '#22262a';
    x = document.getElementById('top_panel').style.backgroundColor = '#33334d';
    x = document.getElementById('leftpanel').style.backgroundColor = '#33334d';
  }
}

}

/*------------------------------ */

// BOARD REORDER FEATURE

let items = document.querySelectorAll('#boards > li')

items.forEach(item => {
  $(item).prop('draggable', true)
  item.addEventListener('dragstart', dragStart)
  item.addEventListener('drop', dropped)
  item.addEventListener('dragenter', cancelDefault)
  item.addEventListener('dragover', cancelDefault)
})

function dragStart (e) {
  var index = $(e.target).index()
  e.dataTransfer.setData('text/plain', index)
}

function dropped (e) {
  cancelDefault(e)
  
  // get new and old index
  let oldIndex = e.dataTransfer.getData('text/plain')
  let target = $(e.target)
  let newIndex = target.index()
  
  // remove dropped items at old place
  let dropped = $(this).parent().children().eq(oldIndex).remove()

  // insert the dropped items at new place
  if (newIndex < oldIndex) {
    target.before(dropped)
  } else {
    target.after(dropped)
  }
}

function cancelDefault (e) {
  e.preventDefault()
  e.stopPropagation()
  return false
}

/*------------------------------ */