<template>
  <div>
    <head><title>Quản lý thương hiệu</title></head>
	<div v-if="showPreload" class="preload-screen">
		<div class="preloader-wrapper d-flex">
			<div class="spinner-border text-primary">
				<span class="visually-hidden">Loading...</span>
			</div>
			<span style="margin-left: 20px; line-height: 30px;">Hệ thống đang xử lý</span>
		</div>
	</div>
    <section class="content-header">
			<div class="container-fluid">
				<div class="row mb-2">
					<div class="col-sm-6">
						<h1>Quản lý thương hiệu</h1>
					</div>
					<div class="col-sm-6">
						<ol class="breadcrumb float-sm-right">
							<li class="breadcrumb-item"><a href='/admin/home'>Quản lý</a></li>
							<li class="breadcrumb-item active">Thương hiệu</li>
						</ol>
					</div>
				</div>
			</div>
		</section>
		
		<section class="search">
			<div id="toast">
    		</div>
			<div class="container">
				<form @submit.prevent="search(search_text)">
					<div class="row">
						<div class="col-6 left pl-4">
							<div class="form-group d-flex justify-content-between">
								<label for="inputPassword6" class="col-form-label">Tên thương hiệu:</label>
								<input type="text" name="name" v-model="search_text" class="form-control">
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
					<div class="card-tools">
						<a data-bs-toggle="modal" data-bs-target="#add" class="btn btn-primary"><span style="font-size: 18px;">+</span> Thêm mới</a>
					</div>
				</div>
				<div class="card-body">
					<table class="table table-hover text-center">
						<thead>
							<tr>
								<th>STT</th>
								<th>Tên thương hiệu</th>
								<th>Ảnh</th>
								<th>Thao tác</th>
							</tr>
						</thead>
						<tbody>
							<template v-if="brand" >
									<tr v-for="(item,index) in brand" :key="item.id">
										<td class="td1" :text="index + ((currentPage - 1) * 3)">{{ index + 1 }}</td>
										<td class="td2">{{item.name}}</td>
										<td class="td2" style="width: 60px; height: 60px;"><img style="width: 100%; height: 100%;" :src="item.img" alt=""></td>
										<td class="td3">
											<a @click="getEditBrand(item.id)" data-bs-toggle="modal" :data-bs-target="'#edit'+item.id" class="btn btn-sm btn-primary mr-2"><i class="fa-solid fa-pen-to-square"></i></a> 
											<a data-bs-toggle="modal" :data-bs-target="'#delete'+ item.id" class="btn btn-sm btn-danger"><i class="fa-solid fa-trash"></i></a>
										</td>
										<div class="modal delete-new" :id="'delete'+item.id">
											<div class="modal-dialog">
												<div class="modal-content">
													<div class="modal-header">
														<h4 class="modal-title">Xóa thương hiệu</h4>
														<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
													</div>
													<div class="modal-body">
														Bạn có chắc là xóa không ?
													</div>
													<div class="modal-footer">
														<button type="button" class="btn btn-danger" data-bs-dismiss="modal">Hủy</button>
														<button @click="clickDeleteBrand(item.id)" class="btn btn-primary">Xác nhận</button>
													</div>
												</div>
											</div>
										</div>
										<div class="modal" :id="'edit'+ item.id">
											<div class="modal-dialog">
												<div class="modal-content">
													<form @submit.prevent="clickEditBrand(brandDto)" enctype="multipart/form-data">
														<div class="modal-header">
															<h4 class="modal-title">Chỉnh sửa thương hiệu</h4>
															<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
														</div>
														<div class="modal-body">
															<div id="logins-part" class="content" role="tabpanel" aria-labelledby="logins-part-trigger">
																<div class="form-group">
																	<label for="">Id</label> 
																	<input type="text" name="id" v-model="brandDto.id" class="form-control" readonly="readonly" />
																</div>
																<div class="form-group">
																	<label for="">Tên</label> 
																	<input type="text" name="name" v-model="brandDto.name" class="form-control" required="required" />
																</div>
																<div class="form-group">
																	<label for="">Ảnh</label> 
																	<input class="form-control" @change="chooseFile($event,1)" type="file" name="fileImage" />
																</div>
																<div class="form-group d-flex justify-content-center">
																	<img id="imageEdit" class="imageEdit" :src="brandDto.img" style="height: 200px; width: 200px"/>
																</div>
															</div>
														</div>
														<div class="modal-footer">
															<button type="button" class="btn btn-danger" data-bs-dismiss="modal">Đóng</button>
															<button type="submit" class="btn btn-primary">Xác nhận</button>
														</div>
													</form>
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

		<div class="modal" id="add">
			<div class="modal-dialog">
				<div class="modal-content">
					<form @submit.prevent="addBrand(brandDtoAdd)" enctype="multipart/form-data">
						<div class="modal-header">
							<h4 class="modal-title">Thêm thương hiệu</h4>
							<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
						</div>
						<div class="modal-body">
							<div id="logins-part" class="content" role="tabpanel" aria-labelledby="logins-part-trigger">
								<div class="form-group">
									<label for="">Tên thương hiệu</label> 
									<input type="text" v-model="brandDtoAdd.name" name="name" class="form-control" placeholder="" required="required" />
								</div>
								<div class="form-group">
									<label for="">Link ảnh</label> 
									<input class="form-control" @change="chooseFile($event,0)" type="file" name="fileImage" />
								</div>
							</div>
						</div>
						<div class="modal-footer">
							<button type="button" class="btn btn-danger" data-bs-dismiss="modal">Đóng</button>
							<button type="submit" class="btn btn-primary">Xác nhận</button>
						</div>
					</form>
				</div>
			</div>
		</div>
  </div>
</template>

<script>
import brandsApi from "../../../service/Brands";
import { showSuccessToast, showErrorToast, showErrorToastMess } from "../../../assets/web/js/main";
export default {
    data(){
        return {
            brand: [],
			brandDtoAdd:{},
			brandDto:{},
			currentPage:'',
            totalPage: '',
            paginationButtons:[],
			search_text:"",
			showPreload: false
        }
    },
    methods: {
		async getListBrand(currentPage, search){
            try{
                const res = await brandsApi.getListBrands(currentPage,search)
                this.brand = res.data.listBrands.content
                this.currentPage = res.data.currentPage
                this.totalPage = res.data.listBrands.totalPages
                this.setupPagination(this.totalPage)
            }
            catch(err){
                console.log("err: "+err)
            }
        },
        async search(name){
            await this.getListBrand(this.currentPage, name)
        },
        async addBrand(brandDtoAdd){
            try{
				this.showPreload = true
				const formData = new FormData();
				brandDtoAdd.img = this.imgDto
				formData.append('name', brandDtoAdd.name);
				formData.append('fileImage', brandDtoAdd.img);
				console.log(formData.get('fileImage')); 
                const res = await brandsApi.postAddBrands(formData)
                    if(res.success){
                        await this.getListBrand(this.currentPage,"")
						this.brandDtoAdd = {}
						this.imgDto=''
						showSuccessToast("Thêm thành công")
                        bootstrap.Modal.getInstance(document.getElementById("add")).hide()
                    }
                    if(res.err) showErrorToastMess('Thêm thất bại')
                    
					this.showPreload = false
            }
            catch(err){
				this.showPreload = false
                console.log("err: "+err)
            }
        },
        async getEditBrand(id){
            try{
                const res = await brandsApi.getEditBrands(id)
                this.brandDto = res.data.brandDto
            }
            catch(err){
                console.log("err: "+err)
            }
        },
        async clickEditBrand(brandDto){
            try{
				this.showPreload = true
				const formData = new FormData();
				if(this.imgDto != "" && this.imgDto != null)
					brandDto.img = this.imgDto
				formData.append('fileImage', brandDto.img);
				formData.append('name', brandDto.name);
				formData.append('id', brandDto.id);
                const res = await brandsApi.postEditBrands(formData)
                    if(res.success){
                        await this.getListBrand(this.currentPage,"")
				        showSuccessToast('Sửa thành công')
                        bootstrap.Modal.getInstance(document.getElementById("edit"+brandDto.id)).hide()
                    }
                    if(res.err) showErrorToastMess("Sửa thất bại")
                    
					this.showPreload = false
            }
            catch(err){
				this.showPreload = false
                console.log("err: "+err)
            }
        },
        async clickDeleteBrand(id){
            try{
				bootstrap.Modal.getInstance(document.getElementById('delete' + id)).hide()
                const res = await brandsApi.deleteBrands(id)
                    if(res.success){
                        await this.getListBrand(this.currentPage,"")
				        showSuccessToast('Xóa thành công')
                    }
                    if(res.err) showErrorToastMess("Xóa thất bại")
            }
            catch(err){
                showErrorToast()
            }
        },
		chooseFile(e,data){
			const file = e.target.files[0];
			if (file) {
				this.imgDto = file;
				if(data == 0)
					this.brandDtoAdd.img = URL.createObjectURL(file)
				if(data == 1)
					this.brandDto.img = URL.createObjectURL(file)
			}
		},
        PaginationButton (page) {
			return {
				page,
				isActive: this.currentPage === page,
				handleClick: async () => {
					console.log("page: "+page)
					await this.loadbrand(page);
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
		async loadbrand(page) {
            try{
                const res = await brandsApi.getListBrands(page,this.search_text)
                this.brand = res.data.listBrands.content
                this.currentPage = res.data.currentPage
                this.totalPage = res.data.listBrands.totalPages
            }
            catch(err){
                console.log("err: "+err)
            }
    	},
    },
	mounted() {
		if(!sessionStorage.getItem("login") && sessionStorage.getItem("role")!="ROLE_ADMIN")
		{
			// window.location.href = "/auth/sign-in"
			this.$router.push("/auth/sign-in")
			sessionStorage.setItem("auth",true)
		}
		else
			this.getListBrand(this.currentPage,this.search_text)
 	},
}
</script>

<style>

</style>