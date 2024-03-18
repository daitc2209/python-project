<template>
	<aside class="main-sidebar menu-admin">
		<a href="/home" class="brand-link" style="text-align: center;">
			<span class="brand-text" style="font-weight: 800;">TCD Laptopshop</span>
		</a>
		<div class="sidebar">
			<div class="user-panel mt-3 pb-3 mb-3 d-flex">
				<div class="info">
					<router-link to="/admin/home" class="d-block"><i class="fa-solid fa-house mr-2"></i><label
						style="color: #fff; cursor: pointer;">TỔNG QUAN</label></router-link>
				</div>
			</div>

			<nav class="mt-2">
				<ul class="nav nav-pills nav-sidebar flex-column" data-widget="treeview" role="menu" data-accordion="false">
					<!-- Add icons to the links using the .nav-icon class with font-awesome or any other icon font library -->
					<label for="" style="color: #fff;">QUẢN LÝ</label>
					<li class="nav-item" id="">
						<router-link to="/admin/category" class="nav-link">
							<i class="nav-icon fa-solid fa-bars"></i>
							DANH MỤC
						</router-link>
					</li>
					<li class="nav-item">
						<router-link to="/admin/brand" class="nav-link">
							<i class="nav-icon fa-solid fa-bars"></i>
							THƯƠNG HIỆU
						</router-link>
					</li>
					<li class="nav-item">
						<router-link to="/admin/product" class="nav-link">
							<i class="nav-icon fa-solid fa-bars"></i>
							SẢN PHẨM
						</router-link>
					</li>
					<li class="nav-item">
						<router-link to="/admin/order" class="nav-link">
							<i class="nav-icon fa-solid fa-bars"></i>
							ĐƠN HÀNG
						</router-link>
					</li>
					<li class="nav-item">
						<router-link to="/admin/user" class="nav-link">
							<i class="nav-icon fa-solid fa-bars"></i>
							NGƯỜI DÙNG
						</router-link>
					</li>
					<li class="nav-item">
						<router-link to="/admin/news" class="nav-link">
							<i class="nav-icon fa-solid fa-bars"></i>
							TIN TỨC
						</router-link>
					</li>
					<label for="" style="color: #fff;">THỐNG KÊ</label>
					<li class="nav-item">
						<router-link to="/admin/revenue/categories" class="nav-link">
							<i class="nav-icon fa-solid fa-bars"></i>
							DANH MỤC
						</router-link>
					</li>
					<li class="nav-item">
						<router-link to="/admin/revenue/products" class="nav-link">
							<i class="nav-icon fa-solid fa-bars"></i>
							SẢN PHẨM
						</router-link>
					</li>
					<!-- <label for="" style="color: #fff;">Quản trị</label>
					<li class="nav-item">
						<router-link to="/admin" class="nav-link">
							<i class="nav-icon fa-solid fa-bars"></i>
							Admin
						</router-link>
					</li> -->
					<div class="brand-link"></div>
					<li class="nav-item">
						<a @click="logout()" class="nav-link" style="cursor: pointer;">
							<i class="nav-icon fa-solid fa-power-off"></i>
							LOGOUT
						</a>
					</li>
				</ul>
			</nav>
		</div>
	</aside>
</template>
  
<script>
import userApi from '../../../service/User'
import axios from 'axios';
export default {
	methods: {
		async logout(){
			try{
				axios.defaults.headers.Authorization = `Bearer ${sessionStorage.getItem("jwtToken")}`;
				const res = await userApi.logout(sessionStorage.getItem("jwtToken"))
					
				if(res.responseCode == "0")
				{
					window.location.href = "/auth/sign-in"
					sessionStorage.removeItem("login"),
					sessionStorage.removeItem("jwtToken"),
					sessionStorage.removeItem("refreshToken"),
					sessionStorage.removeItem("role"),
					sessionStorage.removeItem("img"),
					sessionStorage.removeItem("name"),
					sessionStorage.removeItem("auth"),
					sessionStorage.setItem("logout",true)
				}
			}
			catch(err){
				console.log("err: "+err)
			}
		},
	}
}
var buttons = document.getElementsByClassName('nav-link');

for (var i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener('click', function() {
    // Xóa lớp 'active' từ tất cả các phần tử
    for (var j = 0; j < buttons.length; j++) {
      buttons[j].classList.remove('active');
    }
    
    // Thêm lớp 'active' vào phần tử đã được nhấp
    this.classList.add('active');
  });
}
</script>
  
<style>
.menu-admin{
	background-color: #1c1c50;
}
.nav>.nav-item .nav-link{
	color: #fff;
}
</style>