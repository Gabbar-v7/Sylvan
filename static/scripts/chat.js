// URLS
const route = window.location.origin;
const load = route+'/chat/get/previous/';
const send = route+'/chat/put/';

const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

const user_id = localStorage.getItem("user_id");
var chat_id = 0;
var receiverName = 'Gabbar';
var receiverAvatar = '/static/images/Icon.jpeg';
let previousMessages; 
var loaded = false;


var $messages = $('.messages-content'),
    d, m, i = 0;


function openChat(chat_id_, receiverName_, receiverAvatar_){
 chat_id = chat_id_; receiverName = receiverName_; receiverAvatar = receiverAvatar_;
 document.getElementById('mCSB_1_container').innerHTML = '';
 d = 0;
 loadPrevious();
 initiate();
 document.getElementById('chat').style.height='';
document.getElementById('chat-background').style.height='';
loaded = true;
}

$(window).on('load', async function() {
  $messages.mCustomScrollbar();
  console.log('Website loaded');
  document.getElementById('chat').style.height=0;
  document.getElementById('chat-background').style.height=0;
});

function initiate(){
  document.getElementById('receiverName').innerHTML =  receiverName;
  document.getElementById('avatar-icon').src = receiverAvatar;
  setTimeout( function() {
  previousMessages.forEach(loadMessages);
  }, 100);
  
  function loadMessages(value, index, array){
    if(value['user_id'] == user_id && value['user_id']) senderMessage(msg=value['message'], date=value['date']);
    else receiverMessage(msg = value['message'], date=value['date']);
  }
}

function setDate(date){
  date = new Date( date? date : new Date());
  if (date.getDate() != d || date.getMonth() != m) {
    d = date.getDate(); m = date.getMonth();
    $('<div class="timestamp">' + months[date.getMonth()] + ' ' + date.getDate() + '</div>').appendTo($('#mCSB_1_container'));
  }
}

async function  senderMessage(msg = $('.message-input').val(), date='') {
  if ($.trim(msg) == '') {
    return false;
  }

  var options = {
    method:'POST',
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(msg)
  };
  if(loaded){fetch(send+user_id, options)
  .then(async response => {
    if (response.ok) {
      console.log('Message sent successfully');
    } else {
      console.log(`Error sending message: ${response.status}`);
      return false;
    }
  })
  .catch(error => {
    console.error('Error sending message:', error);
    return false;
  });}
  setDate(date);
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  $('.message-input').val(null);
  updateScrollbar();
}

function receiverMessage(msg, date='') {
  var image_url = document.getElementById('avatar-icon').src;
   $('<div class="message loading new"><figure class="avatar"><img src='+image_url+' /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  if(date){
    date.toLocaleString("en-US", {timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone});
  }

   setTimeout( function () {
    setDate(date);
     $('.message.loading').remove();
     $('<div class="message new"><figure class="avatar"><img src=' + image_url + ' /></figure>' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    updateScrollbar();
  }, 1000);
}

async function loadPrevious(){
  var options = {
    method:'GET',
    headers: {
      "Content-Type": "application/json",
    },
  };
  fetch(load+chat_id, options)
  .then(async response => {
    if (response.ok) {
      previousMessages = await response.json() ;
      console.log('Previous messages loaded');
    } else {
      console.log(`Error loading previous messages: ${response.status}`);
      return false;
    }
  })
  .catch(error => {
    console.error('Error loading previous messages:', error);
    return false;
  });
}

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

$('.chat').click(function() {
  document.getElementById('focus').focus();
 });
 
 $('.chat-close').click(
   function(){ loaded=false;
     document.getElementById('chat').style.height=0;
     document.getElementById('chat-background').style.height=0;}
 );
 
 $('.message-submit').click(function() {
   if(loaded){senderMessage();}
 });
 
 $(window).on('keydown', function(e) {
   if (e.which == 13) {
     if(loaded){senderMessage();}
     return false;
   }
 });