<template>
  <nav class="navbar navbar-expand-lg menu" id="navbar">
		<div class="navbar-menu container-fluid"> 
			<!-- <a class="navbar-brand" href="/home"> -->
				<!-- <img src="../../../images/anh.jpg" width="180px" height="50px"></a> -->
				
				<button 
				class="navbar-toggler" 
				type="button" 
				data-bs-toggle="collapse"
				data-bs-target="#navbarSupportedContent"
				aria-controls="navbarSupportedContent" 
				aria-expanded="false"
				aria-label="Toggle navigation">
				<span><i class="fa-solid fa-bars" style="color: white;"></i></span>
			</button>
			<div class="collapse navbar-collapse" id="navbarSupportedContent">
				<ul class="navbar-menu__nav navbar-nav me-auto mb-2 mb-lg-0">
					<li class="navbar-menu__nav-item"><a class="nav-link active" aria-current="page" href="/home">Trang chủ</a></li>
					<li class="navbar-menu__nav-item"><a class="nav-link" href="/store">Cửa hàng</a></li>
					<!-- <li class="nav-item dropdown">
						<a 
							class="nav-link dropdown-toggle" 
							href="#" id="navbarDropdown" 
							role="button" 
							data-bs-toggle="dropdown" 
							aria-expanded="false">
							Category 
						</a>
						<ul class="dropdown-menu" aria-labelledby="navbarDropdown" style="background-color: #1c1c50;">
							<li><a class="dropdown-item" href="#">Laptop</a></li>
							<li><a class="dropdown-item" href="#">Keyboard</a></li>
							<li><a class="dropdown-item" href="#">Mouse</a></li>
							<li><a class="dropdown-item" href="#">USB</a></li>
						</ul>
					</li> -->
					<li class="navbar-menu__nav-item"><a class="nav-link" href="/about">Giới thiệu</a></li>
					<li class="navbar-menu__nav-item"><a class="nav-link" href="/contact">Liên hệ</a></li>
					<li class="navbar-menu__nav-item"><a class="nav-link" href="/news">Tin tức</a></li>
				</ul>
	
				<div class="d-flex form-search ">
					<input class="form-control me-2 text-search inputSearch" style="width: 92%;" id="inputSearch"
					name="inputSearch" type="text" 
					placeholder="Tìm kiếm" aria-label="Search" v-model="searchText">
					<div class="search__product-list" v-show=" hasResults && searchText !== ''">
						<ul class="search__product-list-item">
							<li class="search__product-item" v-for="product in searchResults" :key="product.id">
								<a class="search__product-item-link" :href="`/store/${product.id}`">
										<img :src="product.img" alt="" class="search__product-img">
										<div class="search__product-item-info">
											<div class="search__product-item-head">
												<h3 class="search__product-item-name">{{ product.name }}</h3>
											</div>

											<div class="search__product-item-body">
												<span class="search__product-item-price">
													{{ formatCurrency(product.price - product.price * product.discount / 100) }}
												</span>
												<span class="search__product-item-price-discount" v-if="product.discount" style="font-weight:600; padding-left:4px">
													{{ formatCurrency(product.price) }}
												</span>
											</div>
										</div>
								</a>
							</li>
						</ul>
					</div>

					<button class="btn btn-outline-success" @click="searchText1" type="submit" id="search-btn" hidden></button>
				
				</div>
				
			</div>
		</div>
	</nav>
</template>

<script>
import searchApi from '../../../service/Search'
import { formatCurrency } from "../../../assets/admin/js/format-admin";
export default {
	data() {
		return {
			searchText: '',
			searchResults: [],
			hasResults: false,
		};
	},
	methods:{
		formatCurrency,
		async searchText1() {
			if(this.searchText=="" || this.searchText==null)
				this.hasResults = false
			
			const res = await searchApi.Search({
				params: {
					term: this.searchText
				}
			})
			if(res != null)
			{
				this.searchResults = res.data.listSearch;
				this.hasResults = true;
			}

		},
	},
	watch: {
		searchText() {
			this.searchText1();
		}
	},

}
</script>

<style>
</style>