<template>
  <div>
    <head><title>Quên mật khẩu</title></head>
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
			<div class="breadcrumbs d-flex flex-row align-items-center col-12">
				<ul>
					<li><a href="/home">Trang chủ</a></li>
					<li class="active"><a href="#">
					<i class="fa fa-angle-right" aria-hidden="true"></i>Quên mật khẩu</a></li>
				</ul>
			</div>
			<div class="col-md-4 col-12 p-0" id="side1">
				<div>
					<h3>Chào mừng trở lại!!</h3>
					<p>Bạn đã có tài khoản?</p>
					<router-link to="/auth/sign-in"><button id="btn">Đăng nhập</button></router-link>
				</div>
			</div>
			<div class="col-md-8 col-12 p-0" id="side2">
				<div class="form-login">
					<h3>Quên mật khẩu</h3>
					<div v-if="error">
						<div class="alert alert-danger">{{error}}</div>
					</div>
					<div v-if="success">
						<div class="alert alert-success">{{success}}</div>
					</div>
					<form v-else @submit.prevent="forgotPW()">
						<p>Chúng tôi sẽ gửi link đổi mật khẩu cho bạn.</p>
						<div class="inp">
							<input v-model="email" type="email" placeholder="Enter your e-mail" name="email" required pattern="^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$">
						</div>
						<div id="login">
							<button type="submit">Gửi</button>
						</div>
					</form>
				</div>
			</div>
		</div>
	</section>
  </div>
</template>

<script>
import ForgotPWApi from '../../../service/ForgotPW'
export default {
	data(){
		return {
			showPreload: false,
			email:'',
			success: '',
			error:""
		}
	},
	methods: {
		async forgotPW(){
			try{
				this.showPreload = true
				const res = await ForgotPWApi.handleRequestForgorPW(this.email)
				if(res.success) this.success = res.success
				if(res.error) this.error = res.error
				this.showPreload = false
			}catch(err){
				console.log("err: "+err)
				this.showPreload = false
			}
		}
	}
}
</script>

<style>

</style>