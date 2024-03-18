<template>
  <div>
    <head><title>Quản lý sản phẩm</title></head>
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
					<h1>Quản lý sản phẩm</h1>
				</div>
				<div class="col-sm-6">
					<ol class="breadcrumb float-sm-right">
						<li class="breadcrumb-item"><a href='/admin/home'>Quản lý</a></li>
						<li class="breadcrumb-item active">Sản phẩm</li>
					</ol>
				</div>
			</div>
		</div>
	</section>

    <section class="search">
		<div class="container">
			<form @submit.prevent="search(1,formSearchProduct)">
				<div class="row">
					<div class="col-6 left px-4">
						<div class="form-group d-flex justify-content-between">
							<label for="" class="col-form-label">Tìm kiếm</label> 
							<input type="text" v-model="formSearchProduct.search_text" class="form-control" placeholder="Nhập tên, mô tả">
						</div>
						<div class="form-group d-flex justify-content-between">
							<label for="" class="col-form-label">Danh mục:</label> 
							<select class="form-control form-select" v-model="formSearchProduct.categoryId">
								<option selected="selected" value=""></option>
									<option v-for="item in this.categories" :key="item.id" :value="item.id">{{item.name}}</option>
							</select>
						</div>
					</div>
					<div class="col-6 right px-4">
						<div class="form-group d-flex justify-content-between">
							<label for="" class="col-form-label">Thương hiệu:</label> 
							<select class="form-control form-select" v-model="formSearchProduct.brandId">
								<option selected="selected" value=""></option>
									<option v-for="item in this.brands" :key="item.id" :value="item.id">{{item.name}}</option>
							</select>
						</div>
					</div>
					<div class="d-flex justify-content-center pr-4 mb-3">
						<button class="btn btn-primary px-4">Tìm kiếm</button>
					</div>
				</div>
			</form>
		</div>
	</section>

<section class="content">
	<div id="toast">
    		</div>
			<!-- Default box -->
			<div class="card">
				<div class="card-header ">
					<h3 class="card-title mt-1">Danh sách sản phẩm</h3>
					<div class="card-tools mr-1">
						<a data-bs-toggle="modal" data-bs-target="#add" class="btn btn-primary"><span style="font-size: 18px;">+</span> Thêm mới</a>
					</div>
				</div>
				<div class="card-body">
					<table class="text-center product-table">
						<thead>
							<tr>
								<th>STT</th>
								<th>Img</th>
								<th>Tên sản phẩm</th>
								<th>Danh mục</th>
								<th>Thương hiệu</th>
								<th>Giá</th>
								<th>Số lượng</th>
								<th>Discount</th>
								<th>Mô tả</th>
								<th>Thao tác</th>
							</tr>
						</thead>
						<tbody>
							<template v-if="product">
									<tr :id="'trow_'+item.id" v-for="(item,index) in product" :key="item.id">
										<td class="td1" :text="index + ((currentPage - 1) * 5)">{{ index+1 }}</td>
										<td class="td2"><img :src='item.img' alt=""></td>
										<td class="td3"><h6>{{item.name}}</h6></td>
										<td class="td4"><h6>{{item.categoryName}}</h6></td>
										<td class="td5"><h6>{{item.brandName}}</h6></td>
										<td class="td6"><h6>{{formatCurrency(item.price)}}</h6></td>
										<td class="td7"><h6>{{item.quantity}}</h6></td>
										<td class="td8"><h6>{{item.discount}}%</h6></td>
										<td class="td9"><h6>{{item.description}}</h6></td>
										<td class="td10">
											<a v-if="item.state == `ACTIVED`" @click="stateProduct(item.id,1)" class="btn btn-sm btn-confirmed mr-2"><i class="fa-solid fa-eye"></i></a>
											<a v-else @click="stateProduct(item.id,0)" class="btn btn-sm btn-secondary mr-2"><i class="fa-solid fa-eye-slash"></i></a>
											<a @click="getEditProduct(item.id)" data-bs-toggle="modal" :data-bs-target="`#edit`+item.id"  class="btn btn-sm btn-primary mr-2"><i class="fa-solid fa-pen-to-square"></i></a> 
											<a data-bs-toggle="modal" :data-bs-target="'#delete'+ item.id" class="btn btn-sm btn-danger"><i class="fa-solid fa-trash"></i></a>
										</td>
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
					<form @submit.prevent="addProduct(productDtoAdd)" enctype="multipart/form-data">
						<div class="modal-header">
							<h4 class="modal-title">Thêm sản phẩm</h4>
							<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
						</div>
						<div class="modal-body">
							<div id="logins-part" class="content" role="tabpanel"
								aria-labelledby="logins-part-trigger">
								<div class="form-group">
									<label for="">Tên sản phẩm</label> 
									<input type="text" v-model="productDtoAdd.name" class="form-control" required="required" />
									
								</div>
								<div class="form-group">
									<label for="">Danh mục</label> 
									<select v-model="productDtoAdd.categoryName" class="form-control form-select" required="required">										
										<option v-for="item in categories" :key="item.id" :value="item.name">{{item.name}}</option>
									</select>									
								</div>
								<div class="form-group">
									<label for="">Thương hiệu</label> 
									<select v-model="productDtoAdd.brandName" class="form-control form-select" required="required">				
										<option v-for="item in brands" :key="item.id" :value="item.name">{{item.name}}</option>
									</select>
									
								</div>
								<div class="form-group">
									<label for="">Giá</label> 
									<input type="text" v-model="productDtoAdd.price" class="form-control" required="required" />
									
								</div>
								<div class="form-group">
									<label for="">Discount</label> 
									<input type="text" v-model="productDtoAdd.discount" class="form-control" required="required" />
									
								</div>
								<div class="form-group">
									<label for="">Số lượng</label> 
									<input type="text" v-model="productDtoAdd.quantity" class="form-control" required="required" />
									
								</div>
								<div class="form-group">
									<label for="">Mô tả</label>
									<textarea v-model="productDtoAdd.description" class="form-control" required="required" rows="4"></textarea>
									<div id="quillEditor"></div>
									<input type="hidden" name="quillContent" id="quillContent">
								</div>
								<div class="form-group">
									<label for="">Trạng thái</label> 
									<select v-model="productDtoAdd.state" class="form-control form-select" required="required">
										<option selected value="ACTIVED">Hiển thị</option>
										<option value="DISABLED">Không hiển thị</option>
									</select>
								</div>
								<div class="form-group">
									<label for="">Img</label> 
									<input class="form-control" @change="chooseFile($event,0)" :value="input" type="file" name="fileImage" />
								</div>
								<div class="form-group d-flex justify-content-center">
									<img id="imageAdd" class="imageAdd" :src="productDtoAdd.img" style="height: 200px; width: 200px"/>
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
		<div v-for="item in product" v-bind:key="item.id" >
			<div class="modal" :id="`edit`+item.id">
				<div class="modal-dialog">
					<div class="modal-content">
						<form 
							id="formEditProduct" 
							@submit.prevent="clickEditProduct(productDto)"
							enctype="multipart/form-data"
						>
							<div class="modal-header">
								<h4 class="modal-title">Chỉnh sửa thông tin sản phẩm</h4>
								<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
							</div>
							<div class="modal-body">
								<div id="logins-part" class="content" role="tabpanel" aria-labelledby="logins-part-trigger">
									<div class="form-group">
										<label for="">Id</label> 
										<input type="text" id="idEdit" v-model="productDto.id" class="form-control" readonly="readonly" />
										<div class="text-danger"></div>
									</div>
									<div class="form-group">
										<label for="">Tên sản phẩm</label> 
										<input type="text" id="nameEdit" v-model="productDto.name" class="form-control" required="required" />
										<div class="text-danger"></div>
									</div>
									<div class="form-group">
										<label for="">Danh mục</label> 
										<select v-model="productDto.categoryName" class="form-control form-select" id="categoryEdit" required="required">
											
												<option v-for="item in categories" :key="item.id" :value="item.name">{{item.name}}</option>
										
										</select>
										<div class="text-danger"></div>
									</div>
									<div class="form-group">
										<label for="">Thương hiệu</label> 
										<select v-model="productDto.brandName" class="form-control form-select" id="brandEdit" required="required">
											
												<option v-for="item in brands" :key="item.id" :value="item.name">{{item.name}}</option>
											
										</select>
										<div class="text-danger"></div>
									</div>
									<div class="form-group">
										<label for="">Giá</label> 
										<input type="text" v-model="productDto.price" class="form-control" id="priceEdit" required="required" />
										<div class="text-danger"></div>
									</div>
									<div class="form-group">
										<label for="">Discount</label> 
										<input type="text" v-model="productDto.discount" class="form-control" id="discountEdit" required="required" />
										<div class="text-danger"></div>
									</div>
									<div class="form-group">
										<label for="">Số lượng</label> 
										<input type="text" v-model="productDto.quantity" class="form-control" id="quantityEdit" required="required" />
										<div class="text-danger"></div>
									</div>
									<div class="form-group">
										<label for="">Mô tả</label>
										<textarea v-model="productDto.description" class="form-control" required="required" id="descriptionEdit" rows="4"></textarea>
										<div class="text-danger"></div>
									</div>
									<div class="form-group">
										<label for="">Trạng thái</label>
										<select v-model="productDto.state" class="form-control form-select" required="required">
											<option selected value="ACTIVED">Hiển thị</option>
											<option value="DISABLED">Không hiển thị</option>
										</select>
									</div>
									<div class="form-group">
										<label for="">Img</label> 
										<input hidden="" type="text" id="thumbnailEdit" v-model="productDto.img"> 
										<input class="form-control" @change="chooseFile($event,1)" type="file" name="fileImage" />
									</div>
									<div class="form-group d-flex justify-content-center">
										<img id="imageAdd" class="imageAdd" :src="productDto.img" style="height: 200px; width: 200px"/>
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
			<div class="modal delete-new" :id="'delete'+item.id">
				<div class="modal-dialog">
					<div class="modal-content">
						<div class="modal-header">
							<h4 class="modal-title">Xóa sản phẩm</h4>
							<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
						</div>
						<div class="modal-body">
							Bạn có chắc là xóa không ?
						</div>
						<div class="modal-footer">
							<button type="button" class="btn btn-danger" data-bs-dismiss="modal">Hủy</button>
							<button @click="clickDeleteProduct(item.id)" class="btn btn-primary">Xác nhận</button>
						</div>
					</div>
				</div>
			</div>
		</div>
  </div>

</template>

<script>
import { showSuccessToast, showErrorToastMess } from "../../../assets/web/js/main";
import { formatCurrency } from "../../../assets/admin/js/format-admin";
import productApi from "../../../service/Product";
import brandsApi from "../../../service/Brands";
import categoriesApi from "../../../service/Categories";
export default {
    data(){
        return {
			product: [],
			productDto:[],
			productDtoAdd:[],
			currentPage:'',
			totalPage:'',
			formSearchProduct: [],
			paginationButtons:[],
			brands:[],
			categories:[],
			input: '',
			showPreload: false
        }
    },
    methods: {
        formatCurrency,
		async addProduct(productDtoAdd){
			try{
				this.showPreload = true
				const formData = new FormData();
				if(this.imgDto != "" || this.imgDto != null)
					productDtoAdd.img = this.imgDto
				formData.append('fileImage', productDtoAdd.img);
				formData.append('name', productDtoAdd.name);
				formData.append('categoryName', productDtoAdd.categoryName);
				formData.append('brandName', productDtoAdd.brandName);
				formData.append('price', productDtoAdd.price);
				formData.append('discount', productDtoAdd.discount);
				formData.append('quantity', productDtoAdd.quantity);
				formData.append('description', productDtoAdd.description);
				formData.append('state', productDtoAdd.state);
				
				const res = await productApi.addProduct(formData)
				if(res.success){
					showSuccessToast("Thêm sản phẩm thành công !!")
					this.productDtoAdd=[]
					this.imgDto=''
				}
				if(res.error){
					showErrorToastMess("Thêm sản phẩm thất bại !!")
				}
				this.showPreload = false
				await this.getListProduct(this.currentPage, this.formSearchProduct)
				bootstrap.Modal.getInstance(document.getElementById("add")).hide()
			
			}
			catch(error){
				this.showPreload = false
				console.log("err: "+error)
				showErrorToastMess("Có lỗi xảy ra !!")
			};
		},

		async getEditProduct(id){
			try{
				const res = await productApi.getEditProduct(id)
				this.productDto = res 
			}
			catch(err){
				showErrorToastMess("Lấy danh sách sản phẩm thất bại !!")
				console.log("Err: "+err)
			}
		},

		async clickEditProduct(productDto){
			try{
				this.showPreload = true
				const formData = new FormData();
				if(this.imgDto != "" && this.imgDto != null)
					productDto.img = this.imgDto
				formData.append('fileImage', productDto.img);
				formData.append('id', productDto.id);
				formData.append('name', productDto.name);
				formData.append('categoryName', productDto.categoryName);
				formData.append('brandName', productDto.brandName);
				formData.append('price', productDto.price);
				formData.append('discount', productDto.discount);
				formData.append('quantity', productDto.quantity);
				formData.append('description', productDto.description);
				formData.append('state', productDto.state);
				
				const res = await productApi.postEditProduct(formData)
				if(res.success){
					showSuccessToast("Chỉnh sửa sản phẩm thành công !!")
					await this.getListProduct(this.currentPage, this.formSearchProduct)
				}
				if(res.error){
					showErrorToastMess("Chỉnh sửa sản phẩm thất bại !!")
				}
				this.showPreload = false
				bootstrap.Modal.getInstance(document.getElementById("edit"+productDto.id)).hide()
			
			}
			catch(error){
				this.showPreload = false
				console.log("err: "+error)
				showErrorToastMess("Có lỗi xảy ra !!")
			};
		},

        async clickDeleteProduct(id){
			try{
				bootstrap.Modal.getInstance(document.getElementById('delete' + id)).hide()
				const res = await productApi.deleteProduct(id)
				if(res.success){
					await this.getListProduct(this.currentPage,this.formSearchProduct)
					showSuccessToast("Xóa sản phẩm thành công !!")
				}
				if(res.error){
					showErrorToastMess("Xóa sản phẩm thất bại !!")
				}
			}
			catch(err){
				console.log("err: "+err)
				showErrorToastMess("Có lỗi xảy ra !!")
			}
		},
		async getListProduct(currentPage, formSearchProduct){
			try{
				const res = await productApi.getListProduct(currentPage,formSearchProduct)

				this.product = res.data.listProduct.content
				this.currentPage = res.data.currentPage
				this.totalPage = res.data.listProduct.totalPages
				this.setupPagination(this.totalPage)
			}
			catch(err){
				console.log("Err: "+err); showErrorToastMess("Lấy danh sách sản phẩm thất bại !!")
			}
		},

		async search(currentPage,formSearchProduct){
			await this.getListProduct(currentPage, formSearchProduct)
		},
		async stateProduct(id,state){
			try{
				const res = await productApi.stateProduct(id,state)

				if(state){
					showSuccessToast("Ẩn sản phẩm thành công !!")
				}
				if(!state)
				{
					showSuccessToast("Hiển thị sản phẩm thành công !!")
				}
				await this.getListProduct(this.currentPage, this.formSearchProduct)
			}
			catch(err){
				console.error("Lỗi: ", err);
				showErrorToastMess("Đã xảy ra lỗi khi thay đổi trạng thái sản phẩm. Vui lòng thử lại sau.")
			}
		},

		chooseFile(e,data){
			const file = e.target.files[0];
			if (file) {
				this.imgDto = file;
				if(data == 0)
					this.productDtoAdd.img = URL.createObjectURL(file)
				if(data == 1)
					this.productDto.img = URL.createObjectURL(file)
			}
		},

		async getBrands(){
			try {
				const res = await brandsApi.getAllBrands()
				this.brands = res.data.brands
			}
			catch(err){
				console.log(err)
			}
		},

		async getCategories(){
			try {
				const res = await categoriesApi.getAllCategories()
				this.categories = res.data.categories
			}
			catch(err){
				console.log(err)
			}
		},
        PaginationButton (page) {
			return {
				page,
				isActive: this.currentPage === page,
				handleClick: async () => {
					await this.loadProduct(page);
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
		async loadProduct(page) {
			try{
				const res = await productApi.getListProduct(page,this.formSearchProduct)
				this.product = res.data.listProduct.content
				this.currentPage = res.data.currentPage
				this.totalPage = res.data.listProduct.totalPages
			}
			catch(err){
				console.log(err)
			}
    	},
		init(){
			this.getBrands()
			this.getCategories()
			this.getListProduct(this.currentPage,this.formSearchProduct)
		}
    },
	mounted(){
		if(!sessionStorage.getItem("login") && sessionStorage.getItem("role")!="ROLE_ADMIN")
		{
			this.$router.push("/auth/sign-in")
			sessionStorage.setItem("auth",true)
		}
		else
			this.init()
	}
}
</script>

<style>

</style>