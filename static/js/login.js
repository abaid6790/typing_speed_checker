// ----------------------------
// WAIT FOR DOM (IMPORTANT FIX)
// ----------------------------
document.addEventListener("DOMContentLoaded", function () {

    // ----------------------------
    // SUPABASE INIT (SAFE)
    // ----------------------------
    const supabaseUrl = "YOUR_SUPABASE_URL";
    const supabaseKey = "YOUR_SUPABASE_ANON_KEY";

    const supabase = window.supabase.createClient(supabaseUrl, supabaseKey);


    // ----------------------------
    // SIGNUP
    // ----------------------------
    const signupForm = document.getElementById("signup-form");

    signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = document.getElementById("signup-name").value;
        const email = document.getElementById("signup-email").value;
        const password = document.getElementById("signup-password").value;

        const { data, error } = await supabase.auth.signUp({
            email,
            password,
            options: {
                data: {
                    full_name: name
                }
            }
        });

        if (error) {
            alert("Signup Error: " + error.message);
            return;
        }

        alert("Signup successful! Check your email for verification.");
        switchTab("login");
    });


    // ----------------------------
    // LOGIN
    // ----------------------------
    const loginForm = document.getElementById("login-form");

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("login-email").value;
        const password = document.getElementById("login-password").value;

        const { data, error } = await supabase.auth.signInWithPassword({
            email,
            password
        });

        if (error) {
            alert("Login Error: " + error.message);
            return;
        }

        // Send session to Flask
        await fetch("/set-session", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                access_token: data.session.access_token
            })
        });

        alert("Login successful!");
        window.location.href = "/dashboard";
    });


    // ----------------------------
    // FORGOT PASSWORD
    // ----------------------------
    const forgotForm = document.getElementById("forgot-form");

    forgotForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("forgot-email").value;

        const { error } = await supabase.auth.resetPasswordForEmail(email, {
            redirectTo: "http://localhost:5000/reset-password"
        });

        if (error) {
            alert(error.message);
            return;
        }

        alert("Password reset email sent!");
        switchTab("login");
    });

});
// ----------------------------
// TAB SWITCHING (UNCHANGED UI LOGIC)
// ----------------------------
function switchTab(tab) {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const forgotForm = document.getElementById('forgot-form');
    const toggleLogin = document.getElementById('toggle-login');
    const toggleSignup = document.getElementById('toggle-signup');

    if (tab === 'login') {
        signupForm.classList.add('hidden');
        forgotForm.classList.add('hidden');

        setTimeout(() => loginForm.classList.remove('hidden'), 100);

        toggleLogin.classList.add('active');
        toggleSignup.classList.remove('active');

    } else if (tab === 'signup') {
        loginForm.classList.add('hidden');
        forgotForm.classList.add('hidden');

        setTimeout(() => signupForm.classList.remove('hidden'), 100);

        toggleLogin.classList.remove('active');
        toggleSignup.classList.add('active');
    }
}
// ----------------------------
// PASSWORD TOGGLE (KEEP YOUR UI)
// ----------------------------
function togglePassword(inputId, btnId) {
    const input = document.getElementById(inputId);
    const btn = document.getElementById(btnId);

    btn.addEventListener("click", () => {
        input.type = input.type === "password" ? "text" : "password";
        btn.classList.toggle("active");
    });
}


// ----------------------------
// INPUT ANIMATION (KEEP YOUR UI)
// ----------------------------
document.querySelectorAll('.input-group input').forEach(input => {
    input.addEventListener('input', function () {
        this.classList.toggle('valid', !!this.value);
    });
});