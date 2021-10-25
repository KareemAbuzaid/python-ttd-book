window.Superlists = {};
window.Superlists.initialize = function() {
	$('#id_text').on('keypress', function() {
		$('.has-error').hide();
	});
};
