// URLS
const route = window.location.origin;
const load = route+'/chat/get/previous/';
const send = route+'/chat/put/';

const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

const user_id = localStorage.getItem("user_id");
var chat_id = 1;
var receiverName = 'Gabber';
var receiverAvatar = '/static/images/Icon.jpeg';
var loaded = false;
let previousMessages; 


var $messages = $('.messages-content'),
    d, m, i = 0;

$(window).on('load', async function() {
  $messages.mCustomScrollbar();
  console.log('Website loaded');
  setReceiver();
  await loadPrevious();
  initiate();
  loaded = true;
});

function setReceiver(){
  document.getElementById('receiverName').innerHTML =  receiverName;
  document.getElementById('avatar-icon').src = receiverAvatar;
}

function initiate(){
  if(previousMessages){setTimeout( function() {
  previousMessages.forEach(loadMessages);
  }, 100);}
}

function loadMessages(value, index, array){
  if(value['user_id'] == user_id && value['user_id']!=null) senderMessage(msg=value['message'], date=value['date']);
  else receiverMessage(msg = value['message'], date=value['date']);
}

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(date){
  date = new Date( date? date : new Date());
  if (date.getDate() != d && date.getMonth() != m) {
    d = date.getDate(); m = date.getMonth();
    $('<div class="timestamp">' + months[date.getMonth()] + ' ' + date.getDate() + '</div>').appendTo($('#mCSB_1_container'));
  }
}

async function  senderMessage(msg = $('.message-input').val(), date='') {
  if ($.trim(msg) == '' || !loaded) {
    return false;
  }

  var options = {
    method:'POST',
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(msg)
  };
  fetch(send+user_id, options)
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
  });
  setDate(date);
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  $('.message-input').val(null);
  updateScrollbar();
}

$('.chat').click(function() {
 document.getElementById('focus').focus();
});

$('.chat-close').click(
  close
)

function close(){
  var chat = document.getElementById('chat');
  chat.style.height = 0;
  chat.style.transform = 'translateY(70px)';

  var chat_background = document.getElementById('chat-background');
  chat_background.style.height = 0;
  chat_background.style.transform = 'translateY(70px)';
}

$('.message-submit').click(function() {
  senderMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    senderMessage();
    return false;
  }
});

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
      previousMessages =await response.json();
      console.log(previousMessages);
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
