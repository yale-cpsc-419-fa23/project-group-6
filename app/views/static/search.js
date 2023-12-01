$(document).ready(function() {
    const searchInput = $("#song-search");
    const resultsDiv = $("#search-results tbody");
    const searchButton = $("#search-button");

    searchInput.on("keyup", function(e) {
        const query = $(this).val();
        const isEnterPressed = e.which === 13;

        // If Enter is pressed, search and increment popularity
        if (isEnterPressed) {
            performSearch(query, true);
        } else if (query.length > 2) {
            // If the user is typing, just get top 10 results without incrementing popularity
            performSearch(query, false);
        } else {
            resultsDiv.empty();
        }
    });

    searchButton.on("click", function() {
        const query = searchInput.val();
        performSearch(query, true);
    });

    resultsDiv.on('click', 'p', function() {
        const chosenSong = $(this).text();
        searchInput.val(chosenSong);
        performSearch(chosenSong, true);
    });

    resultsDiv.on('click', '.like-button, .unlike-button', function() {
        const button = $(this);
        const songId = button.data('song-id');
        const isLike = button.hasClass('like-button');

        const endpoint = isLike ? '/like_song' : '/unlike_song';
        $.ajax({
            url: endpoint,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ song_id: songId }),
            success: function(response) {
                // Toggle the button appearance and class based on like/unlike
                if (isLike) {
                    button.text('Unlike').removeClass('like-button').addClass('unlike-button');
                } else {
                    button.text('Like').removeClass('unlike-button').addClass('like-button');
                }
            },
            error: function(error) {
                console.error('Error updating like status:', error);
            }
        });
    });

    function performSearch(query, incrementPopularity) {
        $.get("/search", { song_name: query, increment_popularity: incrementPopularity }, function(data) {
            resultsDiv.empty();

            if (data && data.length > 0) {
                if (incrementPopularity) {
                    data.forEach(song => {
                        let likeButtonHtml = song.liked ? 
                            `<button class="unlike-button" data-song-id="${song.id}">Unlike</button>` :
                            `<button class="like-button" data-song-id="${song.id}">Like</button>`;
                        
                            resultsDiv.append(`
                            <tr>
                                <td>${song.name}</td>
                                <td>${song.upload_date}</td>
                                <td>${song.upload_user}</td>
                                <td>${song.popularity}</td>
                                <td>${song.filepath}</td>
                                <td>${likeButtonHtml}</td>
                            </tr>
                        `);
                    });
                } else {
                    data.forEach(song => {
                        resultsDiv.append(`<p>${song.name}</p>`);
                    });
                }
            } else {
                resultsDiv.append("<p>No results found</p>");
            }
        });
    }
});
