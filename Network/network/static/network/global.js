
function edit_post(post_id){
    document.querySelectorAll('.post-content').forEach(p_cont => {
        if (post_id === p_cont.dataset.pid) {

            p_cont.style.display = 'none';

            document.querySelectorAll('.edit-content').forEach(e_cont => {
                if (post_id == e_cont.dataset.pid) {

                    // Clear the text area & show the editing post view

                    ta = document.querySelector('textarea[data-pid="' + post_id +'"]')
                    ta.value = ''

                    e_cont.style.display = 'block';
                    
                }
            });

        }
    });
}

function save_edit(post_id) {

    ta = document.querySelector('textarea[data-pid="' + post_id +'"]')

    fetch(`/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            text: ta.value,
        })
    })
    .then(response => {
        if (response.status === 200) {
            return response.json();
        } else {
            throw new Error("Unauthorized Request")
        }
    })
    .then(post => {

        console.log(post)

        // Change post

        document.querySelectorAll('.edit-content').forEach(e_cont => {
            if (post_id === e_cont.dataset.pid) {
    
                e_cont.style.display = 'none';
    
                document.querySelectorAll('.post-content').forEach(p_cont => {
                    if (post_id == p_cont.dataset.pid) {
                        h5 = document.querySelector('h5[data-pid="' + post_id +'"]')
                        h5.innerHTML = post.text;
                        p_cont.style.display = 'block';
                    }
                });
    
    
            }
        });
        
    });    

}