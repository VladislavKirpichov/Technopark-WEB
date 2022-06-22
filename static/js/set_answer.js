$(".set-wright").on("click", function (ev) {
    const $this = $(this)

    const request = new Request(
        'http://127.0.0.1:8000/setwrightanswer/',
        {
            method: 'post',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'answer_id=' + $this.data('id')
        }
    )
    fetch(request).then(function (response) {
            response.json().then(function (parsed) {
                if (parsed.new_status === true) {
                    $(`#correct${$this.data('id')}`).css({"opacity": "100%"});
                    $this.toggleClass("set-wright set-wrong")
                    $this.text("Set as wrong answer")
                }
            });
        })
})

$(".set-wrong").on("click", function (ev) {
    const $this = $(this)

    const request = new Request(
        'http://127.0.0.1:8000/setwronganswer/',
        {
            method: 'post',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'answer_id=' + $this.data('id')
        }
    )
    fetch(request).then(function (response) {
            response.json().then(function (parsed) {
                if (parsed.new_status === false) {
                    $(`#correct${$this.data('id')}`).css({"opacity": "0%"});
                    $this.toggleClass("set-wrong set-wright")
                    $this.text("Set as wright answer")
                }
            });
        })
})