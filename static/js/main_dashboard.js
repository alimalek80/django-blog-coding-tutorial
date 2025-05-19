
    // Hide the actual file input visually but keep it accessible
    const imageInput = document.getElementById('id_image');
    if (imageInput) {
        imageInput.style.opacity = 0;
        imageInput.style.position = 'absolute';
        imageInput.style.zIndex = -1;

        imageInput.addEventListener('change', function () {
            const file = this.files[0];
            const preview = document.getElementById('image-preview');

            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }
