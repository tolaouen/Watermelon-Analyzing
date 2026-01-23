document.addEventListener("DOMContentLoaded", () => {
    // Password validation for login
    const pwd = document.querySelector('input[name="password"]')
    if (pwd) {
        pwd.addEventListener("input", () => {
            const msg = document.querySelector("#passwordHelper")
            if (!msg) return;

            const v = pwd.value;
            const strong = v.length >= 8 && /[A-Z]/.test(v) && /[0-9]/.test(v) && /[!@#$%^&*(),.?<>{}|_=+-/]/.test(v);

            msg.textContent = strong ? "Strong Password ✅" : "Use at least 8 chars, with lower, upper, number, special symbol";
            msg.className = strong ? "form-text text-success" : "form-text text-danger";
        })
    }

    // Set active aside bar
    const asideLinks = document.querySelectorAll('.aside-link ul li a');
    const currentPath = window.location.pathname;

    if (currentPath.startsWith('/user/')) {
        asideLinks[0]?.classList.add('active');
    } else if (currentPath === '/disease/create' || currentPath.startsWith('/disease/create/')) {
        asideLinks[2]?.classList.add('active');
    } else if (currentPath.startsWith('/disease/')) {
        asideLinks[1]?.classList.add('active');
    }

    // Set active navbar
    const navLinks = document.querySelectorAll('.nav-link ul li a');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href) {
            const linkPath = new URL(href, window.location.origin).pathname;
            if (currentPath.startsWith(linkPath) && linkPath !== '/') {
                link.classList.add('active');
            }
        }
    });
})

