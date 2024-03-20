<template>
  <header class="top-navbar">
	<div class="container-fluid">
		<a href="/home"><h1 class="shop-name">TCD Shop</h1></a>
		<div class="other-links">
			<template  v-if="(checklogin == null)  || (checklogin == '') || (checklogin == false)">
				<a href="/auth/sign-in"><button id="btn-login">Đăng nhập</button></a> 
				<a href="/auth/sign-up"><button id="btn-signup">Đăng ký</button></a> 
				
			</template >
			<template  v-if="(checklogin)">
				<ul class="header__navbar-list">
					<li class="header__navbar-item header__navbar-user">
                            <span class="header__navbar-user-name">Xin chào, {{ this.name }}</span>

                            <ul class="header__navbar-user-menu">
                                <li class="header__navbar-user-item">
                                    <a href="/user/profile" class="header__navbar-item-link">Tài khoản của tôi</a>
                                </li>
								<li v-if  ="isAuthenticated == 'admin'" class="header__navbar-user-item">
                                    <a href="/admin/home" class="header__navbar-item-link">Trang quản trị</a>
                                </li>
                                <li class="header__navbar-user-item">
                                    <a href="/user/purchase-history" class="header__navbar-item-link">Đơn mua của tôi</a>
                                </li>
                                <li class="header__navbar-user-item header__navbar-user-item--separate">
                                    <a @click="logout()" class="header__navbar-item-link">Đăng xuất</a>
                                </li>
                            </ul>
                        </li>
				</ul>
				<div class="header__navbar-item header__navbar-user">
					<div @click="click1()"><i class="header__navbar-item-link fa-solid fa-heart"></i> <span style="color:#000; font-weight: 600; padding-left:4px; cursor: pointer;">YÊU THÍCH</span></div>
				</div>
			</template >
			<div class="header__navbar-item header__navbar-user">
				<div @click="click()"><i class="header__navbar-item-link fa-solid fa-cart-shopping"></i> <span style="font-weight: 600; padding-left:4px; cursor: pointer;">GIỎ HÀNG</span></div>
			</div>
		</div>
	</div>

	</header>
</template>

<script>
export default {
	data() {
		return {
			isAuthenticated: sessionStorage.getItem("role"),
			checklogin: "",
			name: sessionStorage.getItem("name"),
			img: sessionStorage.getItem("img"),
		};
  	},
	methods: {
		click(){
			this.$router.push("/cart")
		},
		click1(){
			this.$router.push("/favor")
		},
		async logout(){
			try{
					window.location.href = "/auth/sign-in"
					sessionStorage.removeItem("login"),
					sessionStorage.removeItem("jwtToken"),
					sessionStorage.removeItem("refreshToken"),
					sessionStorage.removeItem("role"),
					sessionStorage.removeItem("name"),
					sessionStorage.removeItem("auth"),
					sessionStorage.setItem("logout",true)
			}
			catch(err){
				console.log("err: "+err)
			}
		},
	},
	mounted() {
		if(sessionStorage.getItem("login")){
			this.checklogin = sessionStorage.getItem("login");
		}
  },
}
</script>

<style>

</style>