
function likeUnlike(el) {
            
    console.log(el.dataset.pid);

    fetch(`/posts/${el.dataset.pid}`, {
        method: 'PUT',
        body: JSON.stringify({
            like: 'clicked',
        })
    })
    .then(response => {
        if (response.status === 200) {
            return response.json();
        } else {
            throw new Error("ERROR")
        }
    })
    .then(result => {
        
        console.log(result)

        likeP = document.querySelector('p[data-pid="' + el.dataset.pid +'"]')
        likeP.innerHTML = `<b>${result.numberOfLikes}</b> Likes`
    })
}


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

    console.log(`/posts/${post_id}`)

    fetch(`/posts/${post_id}`, {
        method: 'POST',
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