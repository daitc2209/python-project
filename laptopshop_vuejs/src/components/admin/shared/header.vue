<template>
	<nav class="main-header navbar navbar-expand navbar-white navbar-light">
		<div>
			<ul class="navbar-nav heading">
				<li class="nav-item"><a class="nav-link" data-widget="pushmenu"
					href="#" role="button"> <i class="fas fa-bars"></i>
				</a></li>
				<li class="nav-item d-none d-sm-inline-block">
				<a href='#' class="nav-link">Trang chủ</a></li>
			</ul>
		</div>
			<!-- <div class="header__navbar-list">
				<li class="header__navbar-item header__navbar-user">
							<div class="input-group input-group-sm">
								<div class="input-group-append">
									<img v-if="this.checkImg" :src="`${this.img}`"
										alt="" class="header__navabar-user-img">
									<img v-else :src="`/src/images/user/${this.img}`"
										alt="" class="header__navabar-user-img">
									<span class="header__navbar-user-name">{{ this.name }}</span>
								</div>
							</div>
				</li>
			</div> -->
	</nav>
		
</template>

<script>
export default {
	// data(){
	// 	return{
	// 		name: sessionStorage.getItem("name"),
	// 		img: sessionStorage.getItem("img"),
	// 		checkImg:/http(s)?:\/\/([\w-]+\.)+[\w-]+(\/[\w- ./?%&=]*)?/.test(this.img)
	// 	}
	// }
}
</script>

<style>
</style>