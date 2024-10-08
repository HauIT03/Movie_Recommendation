document.addEventListener('DOMContentLoaded', function () {
    // Tự động làm mới form khi tải lại trang để xóa mọi thông tin đã nhập
    window.onload = function () {
        document.getElementById('recommendationForm').reset();
        document.getElementById('recommendationList').innerHTML = ''; // Clear recommendations
        document.getElementById('user_id_error').innerHTML = ''; // Clear user_id error message
        document.getElementById('top_n_error').innerHTML = ''; // Clear top_n error message
    };

    document.getElementById('title').addEventListener('input', function () {
        const title = this.value;
        if (title.length > 0) {
            fetch(`/suggest?title=${title}`)
                .then(response => response.json())
                .then(data => {
                    const suggestionsBox = document.getElementById('suggestions');
                    suggestionsBox.innerHTML = '';
                    data.forEach(movie => {
                        const suggestionItem = document.createElement('div');
                        suggestionItem.className = 'suggestion-item';
                        suggestionItem.textContent = movie[1]; // Title
                        suggestionItem.onclick = () => {
                            document.getElementById('title').value = movie[1]; // Set title input
                            suggestionsBox.innerHTML = ''; // Clear suggestions
                        };
                        suggestionsBox.appendChild(suggestionItem);
                    });
                });
        } else {
            document.getElementById('suggestions').innerHTML = ''; // Clear suggestions if input is empty
        }
    });

    document.getElementById('getRecommendationsBtn').addEventListener('click', function () {
        const userIdInput = document.getElementById('user_id');
        const topNInput = document.getElementById('top_n');
        const userIdError = document.getElementById('user_id_error');
        const topNError = document.getElementById('top_n_error');

        // Reset error messages
        userIdError.innerHTML = '';
        topNError.innerHTML = '';

        const formData = new FormData(document.getElementById('recommendationForm'));
        const userId = parseInt(userIdInput.value);
        const topN = parseInt(topNInput.value);

        // Validate inputs
        if (userId < 1 || userId > 610) {
            userIdError.innerHTML = "User ID phải nằm trong khoảng từ 1 đến 610.";
            return;
        }
        if (topN < 1 || topN > 9742) {
            topNError.innerHTML = "Số lượng gợi ý phải nằm trong khoảng từ 1 đến 9742.";
            return;
        }

        const params = new URLSearchParams();
        for (const [key, value] of formData) {
            params.append(key, value);
        }

        fetch('/', {
            method: 'POST',
            body: params
        })
            .then(response => response.text())
            .then(data => {
                document.getElementById('recommendationList').innerHTML = data;
            })
            .catch(error => console.error('Error:', error));
    });
});
document.getElementById('getRecommendationsBtn').addEventListener('click', function () {
    const userIdInput = document.getElementById('user_id');
    const topNInput = document.getElementById('top_n');
    const userIdError = document.getElementById('user_id_error');
    const topNError = document.getElementById('top_n_error');

    // Reset error messages
    userIdError.innerHTML = '';
    topNError.innerHTML = '';

    const formData = new FormData(document.getElementById('recommendationForm'));
    const userId = parseInt(userIdInput.value);
    const topN = parseInt(topNInput.value);

    // Validate inputs
    let hasError = false;
    if (userId < 1 || userId > 610) {
        userIdError.innerHTML = "User ID phải nằm trong khoảng từ 1 đến 610.";
        hasError = true;
    }
    if (topN < 1 || topN > 9742) {
        topNError.innerHTML = "Số lượng gợi ý phải nằm trong khoảng từ 1 đến 9742.";
        hasError = true;
    }

    if (hasError) return; // Ngừng lại nếu có lỗi

    const params = new URLSearchParams();
    for (const [key, value] of formData) {
        params.append(key, value);
    }

    fetch('/', {
        method: 'POST',
        body: params
    })
        .then(response => response.text())
        .then(data => {
            document.getElementById('recommendationList').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
});
