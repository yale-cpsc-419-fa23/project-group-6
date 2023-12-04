$(document).ready(function() {
    const searchInput = $("#song-search");
    const resultsDiv = $("#search-results tbody");
    const searchButton = $("#search-button");


    function setCookie(name, value, days) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    }

    function getCookie(name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for(var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    function autoSearchWithLastQuery() {
        var lastSearchQuery = getCookie('lastSearchQuery');
        if (lastSearchQuery) {
            performSearch(lastSearchQuery, true);
        }
    }

    autoSearchWithLastQuery();

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
            displaySearchResults(data, incrementPopularity);
        });
        setCookie('lastSearchQuery', query, 7);
    }

    function displaySearchResults(data, incrementPopularity) {
        if (data && data.length > 0) {
            if (incrementPopularity) {
                resultsDiv.empty();
                data.forEach(song => {
                    let likeButtonHtml = song.liked ?
                        `<button class="unlike-button" data-song-id="${song.id}">Unlike</button>` :
                        `<button class="like-button" data-song-id="${song.id}">Like</button>`;
                    let creatorsHtml = song.creators.map(creator =>
                        `<a href="/profile/${creator.id}">${creator.username}</a>`
                    ).join(', ');

                    resultsDiv.append(`
                        <tr>
                            <td>${song.name}</td>
                            <td>${creatorsHtml}</td>
                            <td>${song.upload_date}</td>
                            <td>${song.popularity}</td>
                            <td>${song.filepath}</td>
                            <td>${likeButtonHtml}</td>
                        </tr>
                    `);
                });
                $('#search-suggestions').empty();
            } else {
                $('#search-suggestions').empty();
                data.forEach(function(song) {
                    $('<option>').val(song.name).appendTo('#search-suggestions');
                });
            }
        } else {
            resultsDiv.empty();
            resultsDiv.append("<p>No results found</p>");
        }
    }
});