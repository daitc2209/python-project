<template>
	<div>
		<div v-if="showPreload" class="preload-screen">
			<div class="preloader-wrapper d-flex">
				<div class="spinner-border text-primary">
					<span class="visually-hidden">Loading...</span>
				</div>
				<span style="margin-left: 20px; line-height: 30px;">Hệ thống đang xử lý</span>
			</div>
		</div>
		<section class="container login">
			<div class="row">
				<div class="col-md-4 col-12 p-0" id="side1">
					<div>
						<h3>Chào mừng trở lại!!</h3>
	                	<p>Bạn đã có tài khoản?</p>
						<button @click="click" id="btn">Đăng nhập ngay</button>
					</div>
				</div>
				<div class="col-md-8 col-12 p-0" id="side2">
					<div class="form-login">
						<h3>Đăng ký tài khoản</h3>
						<div v-if="error">
			                <div class="alert alert-danger">{{ error }}</div>
			            </div>
						<div v-if="success">
			                <div class="alert alert-success">{{success}}</div>
			            </div>
			            <form v-else @submit.prevent="signUp" class="form-login">
                            <div class="inp">
                                <input v-model="user.name" type="text" required placeholder="Nhập họ và tên" title="VD: Trần Công Đại">
                                <input v-model="user.address" type="text" required placeholder="Nhập địa chỉ" title="VD: Đa Hội Châu Khê">
                                <input v-model="user.email" type="email" placeholder="Nhập Email" required pattern="^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$" title="VD: admin@gmail.com">
                                <input v-model="user.username" type="text" required placeholder="Nhập tên tài khoản" title="VD: trandai">
                                <input @input="clearPasswordMismatchError()" v-model="user.password" autocomplete="" type="password" placeholder="Nhập mật khẩu" required>
                                <input @input="clearPasswordMismatchError()" v-model="user.confirm_password" autocomplete="" type="password" placeholder="Nhập lại mật khẩu" required>
                            </div>
                            <div id="login">
                                <button type="submit">Đăng ký</button>
                            </div>
                        </form>
					</div>
				</div>
			</div>
		</section>
	</div>
</template>

<script>
import userApi from '../../../service/User';
export default {
    data() {
		return {
			showPreload: false,
			user: {
				fullname: '',
				email: '',
				username: '',
				password: '',
				address:'',
				confirm_password: ""
			},
			error: '',
			success: ''
		};
    },
    methods: {
		click(){
			this.$router.push("/auth/sign-in")
		},
		clearPasswordMismatchError() {
			this.error = '';
		},
		async signUp(){
			try{
				if(this.user.fullname != "" || this.user.username != "" || this.user.email !="" || this.user.password != "" || this.user.address != "")
				{
					if (this.user.password !== this.user.confirm_password) {
						this.error = 'Mật khâu không trùng nhau';
						return; 
					}
					this.showPreload = true
					const res = await userApi.signUp(this.user)
					if (res)
						this.success = "Đăng ký thành công"
					else
						this.error = "Có lỗi"

					this.showPreload = false
				}
			}
			catch(err) {
				console.log("err: "+err)
				this.showPreload = false
			}
			
		},
		async checkVerify(){
			try{
				var url = window.location.href

				var urlParam = new URL(url)

				if(urlParam.searchParams.has("token"))
				{
					var token = urlParam.searchParams.get("token");
					const res = await userApi.verify(token)
					if (res.success)
						this.success = res.success
					if (res.error)
						this.error = res.error
				}
			}		
			catch(err) {
				console.log("err: "+err)
			}
				
		},
		
    },
	mounted(){
		if(sessionStorage.getItem("login"))
			window.location.href = '/home'
		else
        	this.signUp();

		this.checkVerify()

	}
}
</script>

<style>

</style>