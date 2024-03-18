<template>
  <div>
    <head><title>Đặt lại mật khẩu</title></head>
    <section class="container login">
			<div class="row">
				<div class="breadcrumbs d-flex flex-row align-items-center col-12">
					<ul>
						<li><a href="/home">Trang chủ</a></li>
						<li class="active"><a href="#">
						<i class="fa fa-angle-right" aria-hidden="true"></i>Đặt lại mật khẩu</a></li>
					</ul>
				</div>
				<div class="col-md-4 col-12 p-0" id="side1">
					<div>
						<h3>Chào mừng trở lại !!!</h3>
						<p>Bạn đã có tài khoản?</p>
						<a href="/auth/sign-in"><button id="btn">Đăng nhập</button></a>
					</div>
				</div>
				<div class="col-md-8 col-12 p-0" id="side2">
					<div class="form-login">
						<h3>Đặt lại mật khẩu</h3>
						<div v-if="success">
							<div class="alert alert-success">{{success}}</div>
						</div>
						<div v-else>
							<div v-if="error">
								<div class="alert alert-danger">{{error}}</div>
							</div>
							<div v-if="tokenError">
								<div class="alert alert-danger">{{tokenError}}</div>
							</div>
							<form v-if="!success && !tokenError" class="form-login" @submit.prevent="resetPW()">
								<div class="inp">
									<input id="password" v-model="newPW" @input="clearPasswordMismatchError()" type="password" placeholder="Enter your new password" name="newPassword" required autofocus pattern="^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])([0-9a-zA-Z]{8,})$" title="Ít nhất 8 ký tự trở lên. Có ít nhất một chữ số. Có ít nhất một chữ cái viết thường. Có ít nhất một chữ cái viết hoa.">
								</div>
								<div class="inp">
									<input v-model="confirmPW" @input="clearPasswordMismatchError()" type="password" placeholder="Confirm your new password" required pattern="^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])([0-9a-zA-Z]{8,})$" title="Ít nhất 8 ký tự trở lên. Có ít nhất một chữ số. Có ít nhất một chữ cái viết thường. Có ít nhất một chữ cái viết hoa.">
								</div>
								<div id="login">
									<button type="submit">Xác nhận</button>
								</div>
							</form>
						</div>
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
            success: "",
            error: "",
			tokenError:"",
			token:"",
			newPW:"",
			confirmPW:""
        }
    },
    methods: {
        async checkTokenPW(){
			try{
				var url = window.location.href

				var urlParam = new URL(url)

				if(urlParam.searchParams.has("token"))
				{
					this.token = urlParam.searchParams.get("token");
					const res = await ForgotPWApi.checkTokenPW(this.token)
					if (res.success) this.success = res.success
					if (res.error) this.tokenError = res.error
				}
			}catch(err){
				console.log("err: "+err)
			}
			
		},
		async resetPW(){
			try{
				if (this.newPW !== this.confirmPW) {
					this.error = 'Mật khẩu không trùng nhau';
					return; 
				}
				const res = await ForgotPWApi.resetPW(this.token, this.newPW)
				if (res.success)
				{
					this.success = res.success
					this.newPW=""
					this.confirmPW=""
				}
				if (res.error) this.tokenError = res.error
			}
			catch(err){
				console.log("err: "+err)
			}
		}
    },
	mounted(){
		this.checkTokenPW()
	}
}
</script>

<style>

</style>