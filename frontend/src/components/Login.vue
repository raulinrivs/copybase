<script setup>
    import { ref } from 'vue';
    import axios from 'axios';
    import router from '@/main';

    const LOGIN_ULR = 'http://127.0.0.1:8000/api/token/';

    const credencials = ref({
        username: '',
        password: ''
    });

    async function login(){
            await axios.post(LOGIN_ULR, {
                username: credencials.value.username,
                password: credencials.value.password
            }).then(function (response) {
                console.log(response);
                localStorage.setItem('access', response.data.access)
                router.push('/dashboard')
            })
            .catch(function (error) {
                console.log(error);
            });
    }

</script>

<template>
    <body class="text-center">
    
        <main class="form-signin">
            <form @submit.prevent="login">
                <h1 class="h3 mb-3 fw-normal">Please sign in</h1>
            
                <div class="form-floating">
                    <input type="text" class="form-control" id="floatingInput" placeholder="Username" v-model="credencials.username">
                    <label for="floatingInput">Username</label>
                </div>
                <div class="form-floating">
                    <input type="password" class="form-control" id="floatingPassword" placeholder="Password" v-model="credencials.password">
                    <label for="floatingPassword">Password</label>
                </div>
            
                <div class="checkbox mb-3">
                    <label>
                        <input type="checkbox" value="remember-me"> Remember me
                    </label>
                </div>
                <button class="w-100 btn btn-lg btn-primary" type="submit">Sign in</button>
                <p class="mt-5 mb-3 text-muted">© 2017–2021</p>
            </form>
        </main>
    </body>
</template>