<template>
    <div class="menu-shared">
         <aside class="main-sidebar sidebar-dark-primary elevation-4">
                <nav class="mt-2">
                    <ul class="menu-container nav nav-pills nav-sidebar flex-column" data-widget="treeview" role="menu" data-accordion="false">
                        <!-- Add icons to the links using the .nav-icon class with font-awesome or any other icon font library -->
                        <li class="menu-item">
                            <router-link to="/home" class="menu-link">
                                <i class="fa-solid fa-house mr-2"></i>
                                <p>Trang chủ</p>
                            </router-link>
                        </li>
                        <li class="menu-item">
                            <router-link to="/user/profile" class="menu-link">
                                <i class="fa-solid fa-user"></i>
                                <p>Thông tin tài khoản</p>
                            </router-link>
                        </li>
                        <li class="menu-item">
                            <router-link to="/user/purchase-history" class="menu-link">
                                <i class="fa-solid fa-clipboard"></i>
                                <p>Quản lý đơn hàng</p>
                            </router-link>
                        </li>
                        
                        <div class="brand-link"></div>
                        <li class="menu-item">
                            <a @click="logout()" class="menu-link" style="cursor: pointer;">
                                <i class="nav-icon fa-solid fa-power-off"></i>
                                <p>Đăng xuất</p>
                            </a>
                        </li>
                    </ul>
                </nav>
        </aside>
    </div>

</template>

<script>
import userApi from '../../../service/User'
import axios from 'axios';
export default {

    methods:{
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
</script>

<style>
.menu-shared{
    padding: 10px;
    background-color: #f6fbfc;
    width: auto;
    height: 100%;
    margin-right: 50px;
}
.main-sidebar{
    position: sticky;
    top: 56px;
}
.menu-container{
    width: 100%;
    height: 100%;
}
.menu-item{
    padding: 5px 0;
}
.menu-link{
    display: flex;
    justify-content: flex-start;
    align-items: center;
    padding: 5px 0;
}
.menu-link p{
    font-size: 20px;
    margin: 0 0 0 10px;
    color: #686868;
    font-weight: 500;
}
.menu-link i{
    color:#7E7171
}
</style>