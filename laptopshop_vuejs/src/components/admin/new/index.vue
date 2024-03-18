<template>
  <div>
	<head><title>Quản lý tin tức</title></head>
    <section class="content-header">
			<div class="container-fluid">
				<div class="row mb-2">
					<div class="col-sm-6">
						<h1>Quản lý tin tức</h1>
					</div>
					<div class="col-sm-6">
						<ol class="breadcrumb float-sm-right">
							<li class="breadcrumb-item"><a href='/admin/home'>Quản lý</a></li>
							<li class="breadcrumb-item active">Tin tức</li>
						</ol>
					</div>
				</div>
			</div>
		</section>
		
		<section class="search">
			<div id="toast">
    		</div>
			<div class="container">
				<form @submit.prevent="search(1,keyword)">
					<div class="row">
						<div class="col-6 left pl-4">
							<div class="form-group d-flex justify-content-between">
								<label for="inputPassword6" class="col-form-label">Tên bài viết, tin tức:</label>
								<input type="text" name="keyword" v-model="this.keyword" class="form-control">
							</div>
						</div>
						<div class="col-6 right pl-4">
							<button class="btn btn-primary px-4" type="submit">Tìm kiếm</button>
						</div>
					</div>
				</form>
			</div>
		</section>

		<section class="content">

			<!-- Default box -->
			<div class="card">
				<div class="card-header">
					<h3 class="card-title">Danh sách tin tức</h3>
					<div class="card-tools">
						<a data-bs-toggle="modal" data-bs-target="#add" class="btn btn-primary"><span style="font-size: 18px;">+</span> Thêm mới</a>
					</div>
				</div>
				<div class="card-body">
					<table class="table news-table table-hover text-center">
						<thead>
							<tr>
								<th>No.</th>
								<th>Ảnh</th>
								<th>Tên bài viết</th>
								<th>Mô tả ngắn</th>
								<th>Thao tác</th>
							</tr>
						</thead>
						<tbody>
							<template v-if="news">
									<tr v-for="(item,index) in news" v-bind:key="item.id">
										<td class="td1" :text="index + ((currentPage - 1) * 3)">{{ index + 1 }}</td>
										<td class="td2"><img :src="item.img" alt=""></td>
										<td class="td3">{{ item.title }}</td>
										<td class="td4">{{ item.shortDescription }}</td>
										<td class="td5">
											<a data-bs-toggle="modal" :data-bs-target="'#edit'+ item.id" @click="getEditNewsAdmin(item.id)" class="btn btn-sm btn-primary mb-2"><i class="fa-solid fa-pen-to-square"></i></a> 
											<a data-bs-toggle="modal" :data-bs-target="'#delete'+ item.id" class="btn btn-sm btn-danger"><i class="fa-solid fa-trash"></i></a>
										</td>
										<div class="modal add-new" :id="'edit'+item.id">
											<div class="modal-dialog">
												<div class="modal-content">
													<form @submit.prevent="postEditNewsAdmin(item.id)"  >
														<div class="modal-header">
															<h4 class="modal-title">Chỉnh sửa tin tức</h4>
															<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
														</div>
														<div class="modal-body">
															<div id="logins-part" class="content" role="tabpanel" aria-labelledby="logins-part-trigger">
																<div class="form-group">
																	<label class="d-flex">ID</label> 
																	<input type="text" id="idEdit" v-model="newDto.id" class="form-control" readonly="readonly" />
																	<div class="text-danger"></div>
																</div>
																<div class="form-group">
																	<label class="d-flex">Thể loại</label> 
																	<select class="form-control form-select" required="required" v-model="newDto.categoryName" id="categoryEdit">
																		<option v-for="item in category" v-bind:key="item.id"
																			 :value="item.name" >{{ item.name }}</option>
																	</select>
																</div>
																<div class="form-group">
																	<label class="d-flex">Tiêu đề</label> 
																	<input type="text" v-model="newDto.title" class="form-control" required="required" id="titleEdit"/>
																	<div class="text-danger"></div>
																</div>
																<div class="form-group">
																	<label class="d-flex">Hình đại diện</label> 
																	<input type="text" v-model="newDto.img" class="form-control" required="required" id="thumbnailEdit"/>
																	<div class="text-danger"></div>
																</div>
																<div class="form-group">
																	<label class="d-flex">Mô tả ngắn</label> 
																	<textarea class="form-control" v-model="newDto.shortDescription" required="required" id="shortDescriptionEdit"></textarea>
																</div>
																<div class="form-group">
																	<label class="d-flex">Nội dung</label> 
																	<textarea class="form-control" :id="`contentEdit`+item.id" v-model="newDto.content"></textarea>
																</div>
															</div>
														</div>
														<div class="modal-footer">
															<button type="button" class="btn btn-danger" data-bs-dismiss="modal">Hủy</button>
															<button type="submit" class="btn btn-primary">Xác nhận</button>
														</div>
													</form>
												</div>
											</div>
										</div>

										<div class="modal delete-new" :id="'delete'+item.id">
											<div class="modal-dialog">
												<div class="modal-content">
													<div class="modal-header">
														<h4 class="modal-title">Xóa tin tức</h4>
														<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
													</div>
													<div class="modal-body">
														Bạn có chắc là xóa không ?
													</div>
													<div class="modal-footer">
														<button type="button" class="btn btn-danger" data-bs-dismiss="modal">Hủy</button>
														<button @click="clickDeleteNew(item.id)" class="btn btn-primary">Xác nhận</button>
													</div>
												</div>
											</div>
										</div>
									</tr>
							</template>
							<template v-else>
								<tr>
									<td colspan="4">Không có bản ghi nào!!!</td>
								</tr>
							</template>

							<div class="modal add-new edit" id="add">
								<div class="modal-dialog">
									<div class="modal-content">
										<form @submit.prevent="postAddNewsAdmin()" >
											<div class="modal-header">
												<h4 class="modal-title">Thêm mới tin tức</h4>
												<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
											</div>
											<div class="modal-body">
												<div id="logins-part" class="content" role="tabpanel" aria-labelledby="logins-part-trigger">
													<div class="form-group">
														<label class="d-flex">Thể loại</label> 
														<select class="form-control form-select" required="required" v-model="newAdd.categoryName">
															<option v-for="item in category" v-bind:key="item.id" :value="item.name" >{{ item.name }}</option>
														</select>
													</div>
													<div class="form-group">
														<label class="d-flex">Tiêu đề</label> 
														<input type="text" v-model="newAdd.title" class="form-control" required="required" />
														<div class="text-danger"></div>
													</div>
													<div class="form-group">
														<label class="d-flex">Hình đại diện</label> 
														<input type="text" v-model="newAdd.img" class="form-control" required="required" />
														<div class="text-danger"></div>
													</div>
													<div class="form-group">
														<label class="d-flex">Mô tả ngắn</label> 
														<textarea class="form-control" v-model="newAdd.shortDescription" required="required"></textarea>
														<div class="text-danger"></div>
													</div>
													<div class="form-group">
														<label class="d-flex">Nội dung</label> 
														<textarea class="form-control" id="contentAdd" v-model="newAdd.content"></textarea>
													</div>
												</div>
											</div>
											<div class="modal-footer">
												<button type="button" class="btn btn-danger" data-bs-dismiss="modal">Hủy</button>
												<button type="submit" class="btn btn-primary">Xác nhận</button>
											</div>
										</form>
									</div>
								</div>
							</div>
						</tbody>
					</table>
				</div>
				<div class="pagination" id="pagination" v-if="paginationButtons.length >= 2">
					<button v-for="page in paginationButtons" :key="page" 
					:class="{ active: currentPage === page }" 
					@click="PaginationButton(page).handleClick()">
						{{ page }}
					</button>
				</div>
			</div>
		</section>

		
  </div>
</template>

<script>
import newsApi from '../../../service/News';
import { showSuccessToast, showErrorToastMess } from "../../../assets/web/js/main";

export default {
    data(){
        return {
			paginationButtons:[],
            news: [],
            newDto: {},
            newAdd: {},
			category:[],
			currentPage:'',
			totalPage:"", 
			keyword:''
        }
    },
    methods: {
		async getNewsAdmin(){
			try{
				const res = await newsApi.getNewsAdmin(this.currentPage,this.keyword)
				if(res){
					this.news = res.data.news.content
					this.totalPage = res.data.totalPage
					this.currentPage = res.data.currentPage
					this.category = res.data.category
					this.setupPagination(this.totalPage)
				}
			}
			catch(err){
				console.log("err: "+err)
				showErrorToastMess("Lấy danh sách bài viết thất bại")
			}
		},
		async getEditNewsAdmin(id){
			try{
				const res = await newsApi.getEditNewsAdmin(id)
				this.newDto = res.data.newsDto
				CKEDITOR.replace('contentEdit' + id, {}, () => {
					CKEDITOR.instances['contentEdit' + id].setData(res.data.newsDto.content);
				});
			}
			catch(err){
				console.log("err: "+err)
			}
		},
		async postEditNewsAdmin(id){
			try{
				this.newDto.content = CKEDITOR.instances['contentEdit' + id].getData();
				const res = await newsApi.postEditNewsAdmin(this.newDto)
				if(res){
					showSuccessToast("Chỉnh sửa bài viết thành công")
					await this.getNewsAdmin()
				}
				bootstrap.Modal.getInstance(document.getElementById("edit"+id)).hide()
			}catch(err){
				console.log("err: "+err)
				showErrorToastMess("Chỉnh sửa bài viết thất bại")
			}
		},
		async postAddNewsAdmin(){
			try{
				this.newAdd.content = CKEDITOR.instances['contentAdd'].getData();
				const res = await newsApi.postAddNewsAdmin(this.newAdd)
				if(res){
					showSuccessToast("Thêm bài viết thành công")
					this.newAdd={}
					await this.getNewsAdmin()
				}
				bootstrap.Modal.getInstance(document.getElementById("add")).hide()
			}catch(err){
				console.log("err: "+err)
				showErrorToastMess("Thêm bài viết thất bại")
			}
		},
        async clickDeleteNew(id){
			try{
				bootstrap.Modal.getInstance(document.getElementById("delete" + id)).hide()
				const res = await newsApi.deleteNewsAdmin(id)
				if(res){
					showSuccessToast("Xóa bài viết thành công")
					await this.getNewsAdmin();
				}
			}catch(err){
				console.log("err: "+err)
				showErrorToastMess("Xóa bài viết thất bại")
			}
		},
        PaginationButton (page) {
			return {
				page,
				isActive: this.currentPage === page,
				handleClick: async () => {
					console.log("page: "+page)
					await this.loadNews(page);

				},
			};
		},
    	setupPagination (totalPage) {
			this.paginationButtons = [];

			let page_count = totalPage;
			for (let i = 1; i < page_count + 1; i++) {
				this.paginationButtons.push(i);
			}
		},
		async loadNews(page) {
			try{
				const res = await newsApi.getNewsAdmin(page)
				if(res){
					this.news = res.data.data.news.content
					this.totalPage = res.data.data.totalPage
					this.currentPage = res.data.data.currentPage
				}
			}catch(err){
				showErrorToastMess("Lấy danh sách bài viết thất bại")
				console.log("err: "+err)
			}
    	},

		initializeEditor(){
			CKEDITOR.replace( 'contentAdd');
		},
		
		async search(page,keyword){
			console.log("keyword: "+keyword)
			await this.getNewsAdmin(page,keyword)
		}
	},
    mounted() {
		if(!sessionStorage.getItem("login") && sessionStorage.getItem("role")!="ROLE_ADMIN")
		{
			this.$router.push("/auth/sign-in")
			sessionStorage.setItem("auth",true)
		}
		else{
			this.initializeEditor()
			this.getNewsAdmin();
		}
 	},
}
</script>

<style>
.news-table img{
	width: 50px;
	height: 50px;
}
</style>