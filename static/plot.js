document.addEventListener('DOMContentLoaded', function () {
    var plotForm = document.getElementById('plotForm');
    var plotContainer = document.getElementById('plotContainer');

    plotForm.addEventListener('submit', function (e) {
        e.preventDefault();
        
        var requestData = {
            stock: document.getElementById('stock').value,
            begin: document.getElementById('begin').value,
            end: document.getElementById('end').value,
            criteria: document.getElementById('criteria').value
        }

        // create a fetch request to the server
        fetch('api/plot', {
            method: 'GET',
            params: requestData
        }).then(function (response) {
            console.log(response);
        })
    });
});
