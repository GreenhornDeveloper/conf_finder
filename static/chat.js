function talk_to_chatbot() {
	// Get input data
	var user_response = $('#user_question').val();
	var user_identifier = $('#user_identifier').val();

	// Clear query input
	$('#user_question').val('');

	// Input validation
	if (user_question === "" || user_question === null || user_question === undefined) {
		$("span").text("Please enter text").show().fadeOut(1000);
		event.preventDefault();
		return;
	}
	else {
		axios.post('/api/askChatbot', {user_response, user_identifier})
		.then(async function(response) {
			var scenarioOver = response.data.substr(response.data.length - 6) == '!OVER!';

			append_message(user_response, 'right');

			if(scenarioOver) {
			    response.data = response.data.substr(0, response.data.length - 6);
			    append_message(response.data, 'left');
			    append_message('Is there anything else I can help you with?', 'left');
			} else{
			    append_message(response.data, 'left');
			    updateLastMessage(response.data);
			}

		})
		.catch(function(error) {
			console.log(error);
		});
		event.preventDefault(); //keeps page from refreshing after success
	}
}

// Scroll helper function
function updateScroll(){
    var element = document.getElementsByClassName('chat_container')[0];
    element.scrollTop = element.scrollHeight;
}

// Get and store user ID for session management
function store_id() {
	// Store ID in hidden input
	$('#user_identifier').val($('#pre-id').html())

	// Swap forms
	$('.blank_form').hide();
	$('.chat_container').show();
	$('#user_question').focus();

	event.preventDefault()
}

function getMessage(text, align) {
	var msg = `<li style="clear: both;">
					<div class="chat-text ${align}">${text}</div>
				</li>`;
	return msg;
}

function append_message(text, align) {
	$('ul').append(getMessage(text, align));
	updateScroll();
}

function updateLastMessage(text) {
	$('.chat-text').last().html(text);
	updateScroll();
}