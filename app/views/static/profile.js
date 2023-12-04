$(document).ready(function() {
    const resultsDiv = $(".main-content");

    resultsDiv.on('click', '.follow-button, .unfollow-button', function() {
        const button = $(this);
        const userId = button.data('user-id');
        const isFollowing = button.hasClass('follow-button');
        const endpoint = isFollowing ? '/follow' : '/unfollow';
        console.log("test1")
        $.ajax({
            url: endpoint,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ user_id: userId }),
            success: function(response) {
                console.log('success')
                if (isFollowing) {
                    button.text('Unfollow').removeClass('follow-button').addClass('unfollow-button');
                } else {
                    button.text('Follow').removeClass('unfollow-button').addClass('follow-button');
                }
            },
            error: function(error) {
                console.error('Error updating like status:', error);
            }
        });
    });


});