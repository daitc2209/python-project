<template>
  <div>
    <head>
        <title>Trang tin tức</title>
    </head>
    <section>
			<div class="container">
				<div class="row">
					<div class="breadcrumbs d-flex flex-row align-items-center col-12 mt-3 mx-3">
						<ul>
							<li><a href="/home">Trang chủ</a></li>
							<li class="active"><a href="#"><i class="fa fa-angle-right" aria-hidden="true"></i>Tin tức</a></li>
						</ul>
					</div>
					<div class="col-12">
						<div class="box-news">
							<div class="box-new-item" v-for="item in news" :key="item.id">
								<div class="row">
									<div class="col-3">
										<img alt="" :src="item.img" @click="submitFormNewDetail(item.id)">
									</div>
									<div class="col-9">
										<div class="new-content">
											<h5><a :href="'/news/detail?id='+item.id+'&page='+this.currentPage">{{item.title}}</a></h5>
											<p>{{item.shortDescription}}</p>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div>
					<div class="pagination" id="pagination" v-if="paginationButtons.length >= 2">
						<button v-for="page in paginationButtons" :key="page" 
						:class="{ active: currentPage === page }" 
						@click="PaginationButton(page).handleClick()">
							{{ page }}
						</button>
					</div>
				</div>
			</div>
		</section>
  </div>
</template>

<script>

import newsApi from '../../../service/News';
export default {
    data(){
        return {
			paginationButtons:[],
            currentPage: "",
            news: [],
			totalPage:""
        }
    },
    methods: {
		async getNews(){
			try{
				const res = await newsApi.getNews(this.currentPage)
				if(res)
				{
					this.news = res.data.listNews
					this.totalPage = res.data.totalPage
					this.currentPage = res.data.currentPage
					this.SetupPagination(this.totalPage)
				}
			}catch(err){
				console.log("err news: "+err)
			}
		},
		PaginationButton (page) {
			return {
				page,
				isActive: this.currentPage === page,
				handleClick: async () => {
					await this.loadNews(page);
				},
			};
		},
		SetupPagination (totalPage) {
			this.paginationButtons = [];

			let page_count = totalPage;
			for (let i = 1; i < page_count + 1; i++) {
				this.paginationButtons.push(i);
			}
		},
		async loadNews(page) {
			try{
				const res = await newsApi.getNews(page)
				if(res)
				{
					this.news = res.data.listNews
					this.totalPage = res.data.totalPage
					this.currentPage = res.data.currentPage
				}
			}catch(err){
				console.log("err news: "+err)
			}
		}
    },
	mounted(){
		this.getNews()
	}
}
</script>

<style>
</style>