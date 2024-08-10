// urls
const route = window.location.origin;
const load = route+'/chat/get/previous/';
const send = route+'/chat/put/';

const user_id = localStorage.getItem("user_id");
const chat_id = localStorage.getItem("chat_id");
var loaded = false;
let previousMessages;

var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).on('load', async function() {
  $messages.mCustomScrollbar();
  console.log('Website loaded');
  await loadPrevious();
  initiate();
  loaded = true;
});

function initiate(){
  setTimeout( function() {
  previousMessages.forEach(loadMessages);
  }, 100);
}

function loadMessages(value, index, array){
  if(value['user_id'] == user_id) senderMessage(msg=value['message'], date=value['date']);
  else receiverMessage(msg = value['message'], date=value['date']);
}

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(date){
  d = new Date( date? date : new Date());
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
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

  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate(date);
  $('.message-input').val(null);
  updateScrollbar();
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
     $('.message.loading').remove();
     $('<div class="message new"><figure class="avatar"><img src=' + image_url + ' /></figure>' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate(date);
    updateScrollbar();
  }, 1000);
}
