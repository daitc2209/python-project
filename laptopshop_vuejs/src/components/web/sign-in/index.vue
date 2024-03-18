<template>
  <section class="container login">
			<div class="row">
				<div class="col-md-4 col-12 p-0" id="side1">
					<div>
						<h3>Chào mừng đến với TCD Shop</h3>
						<p>Bạn chưa có tài khoản?</p>
						<button @click="click" id="btn">Đăng ký ngay</button>
					</div>
				</div>
				<div class="col-md-8 col-12 p-0" id="side2">
					<form class="form-login" @submit.prevent="login">
						<div v-if="param.error">
			                <div class="alert alert-danger">Tên đăng nhập hoặc mật khẩu không đúng !!</div>
			            </div>
			            <div v-if="param.logout">
			                <div class="alert alert-success"> Đăng xuất thành công.</div>
			            </div>
			            <div v-if="param.accessDenied">
			                <div class="alert alert-danger"> Bạn không có quyền.</div>
			            </div>
						<div v-if="param.checkLoginForCheckOut">
			                <div class="alert alert-danger"> Vui lòng đăng nhập </div>
			            </div>
						<h3>Đăng nhập</h3>
						<div class="inp">
							<input v-model="user.username" type="text" name="username" id="username" placeholder="User Name" required> 
							<input v-model="user.password" autocomplete="" type="password" name="password" id="password" placeholder="Password" required>
						</div>
						<div class="m-0 p-2 mt-2"><input type="checkbox" /> Remember me</div>
						<p class="m-0"><a href="/auth/forgot-password">Quên mật khẩu</a></p>
						<div id="login">
							<button type="submit">Đăng nhập</button>
						</div>
					</form>
				</div>
			</div>
		</section>
</template>

<script>

import userApi from '../../../service/User';
export default {
	data() {
        return {
            user: {
                username: '',
                password: ''
            },
            param: {
				error: false,
				logout: false,
				accessDenied: false,
				checkLoginForCheckOut: false
			},
            display: 'none',
        }
    },
	methods: {
		click(){
			this.$router.push("/auth/sign-up")
		},
		async login(){
			try{
				const res = await userApi.login(this.user)
				if(res != null){
					console.log(res)
					sessionStorage.setItem("login", true)
					sessionStorage.setItem("jwtToken", res.data.access_token)
					sessionStorage.setItem("refreshToken", res.data.refresh_token)
					sessionStorage.setItem("name", res.data.name)
					sessionStorage.setItem("role", res.data.role)
					sessionStorage.setItem("auth", true)
					window.location.href = '/home'
				}
			}catch(err) {
				this.param.error = true
				console.log("err: " + err)
			}
		},
	},
	mounted(){
		if (sessionStorage.getItem("login"))
			window.location.href = '/home'
		if(sessionStorage.getItem("logout"))
		{
			this.param.logout = true
			sessionStorage.removeItem("logout")
		}
		if(sessionStorage.getItem("err"))
		{
			this.param.checkLoginForCheckOut = true
			sessionStorage.removeItem("err")
		}
		if(sessionStorage.getItem("auth"))
		{
			this.param.accessDenied = true
			sessionStorage.removeItem("auth")
		}
	}
}
</script>

<style>

</style>