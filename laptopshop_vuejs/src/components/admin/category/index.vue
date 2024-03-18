<template>
  <div>
    <head><title>Quản lý danh mục</title></head>
    <section class="content-header">
        <div class="container-fluid">
            <div class="row mb-2">
                <div class="col-sm-6">
                    <h1>Quản lý danh mục</h1>
                </div>
                <div class="col-sm-6">
                    <ol class="breadcrumb float-sm-right">
                        <li class="breadcrumb-item"><a href='/admin/home'>Quản lý</a></li>
                        <li class="breadcrumb-item active">Danh mục</li>
                    </ol>
                </div>
            </div>
        </div>
    </section>
    
    <section class="search">
        <div id="toast">
    		</div>
        <div class="container">
            <form @submit.prevent="search(name)">
                <div class="row">
                    <div class="col-6 left pl-4">
                        <div class="form-group d-flex justify-content-between">
                            <label for="inputPassword6" class="col-form-label">Tên danh mục:</label>
                            <input type="text" name="name" v-model="name" class="form-control">
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
                <h3 class="card-title">Danh sách danh mục</h3>
                <div class="card-tools">
                    <a data-bs-toggle="modal" data-bs-target="#add" class="btn btn-primary"><span style="font-size: 18px;">+</span> Thêm mới</a>
                </div>
            </div>
            <div class="card-body">
                <table class="table table-hover text-center">
                    <thead>
                        <tr>
                            <th>STT</th>
                            <th>Tên danh mục</th>
                            <th>Thao tác</th>
                        </tr>
                    </thead>
                    <tbody>
                        <template v-if="category">
                                <tr v-for="(item,index) in category" :key="item.id">
									<td class="td1" :text="index + ((currentPage - 1) * 3)">{{ index + 1 }}</td>
                                    <td class="td2">{{item.name}}</td>
                                    <td class="td3">
                                        <a data-bs-toggle="modal" :data-bs-target="'#edit'+item.id" @click="getEditCategory(item.id)" class="btn btn-sm btn-primary mr-2"><i class="fa-solid fa-pen-to-square"></i></a> 
                                        <a data-bs-toggle="modal" :data-bs-target="'#delete'+ item.id" class="btn btn-sm btn-danger"><i class="fa-solid fa-trash"></i></a>
                                    </td>
                                    <div class="modal delete-new" :id="'delete'+item.id">
                                        <div class="modal-dialog">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                    <h4 class="modal-title">Xóa danh mục</h4>
                                                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                                </div>
                                                <div class="modal-body">
                                                    Bạn có chắc là xóa không ?
                                                </div>
                                                <div class="modal-footer">
                                                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal">Hủy</button>
                                                    <button @click="clickDeleteCategory(item.id)" class="btn btn-primary">Xác nhận</button>
                                                </div>
                                            </div>
                                        </div>
									</div>
                                    <div class="modal" :id="'edit'+ item.id">
                                        <div class="modal-dialog">
                                            <div class="modal-content">
                                                <form @submit.prevent="clickEditCategory(categoryDto)" >
                                                    <div class="modal-header">
                                                        <h4 class="modal-title">Chỉnh sửa danh mục</h4>
                                                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                                    </div>
                                                    <div class="modal-body">
                                                        <div id="logins-part" class="content" role="tabpanel" aria-labelledby="logins-part-trigger">
                                                            <div class="form-group">
                                                                <label for="">Id</label> 
                                                                <input type="text" name="id" v-model="categoryDto.id" class="form-control" readonly="readonly" />
                                                                <div class="text-danger"></div>
                                                            </div>
                                                            <div class="form-group">
                                                                <label for="">Tên danh mục</label> 
                                                                <input type="text" name="name" v-model="categoryDto.name" class="form-control" required="required" />
                                                                <div class="text-danger"></div>
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
                <form @submit.prevent="addCategory(categoryDto)">
                    <div class="modal-header">
                        <h4 class="modal-title">Thêm danh mục</h4>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div id="logins-part" class="content" role="tabpanel" aria-labelledby="logins-part-trigger">
                            <div class="form-group">
                                <label for="">Tên danh mục</label> 
                                <input type="text" v-model="categoryDto.name" name="name" class="form-control" placeholder="" required="required" />
                                <div class="text-danger"></div>
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
import categoriesApi from '../../../service/Categories'
import { showSuccessToast, showErrorToast } from "../../../assets/web/js/main";
export default {
    data(){
        return {
            category: [],
            categoryDto: {},
            currentPage:'',
            totalPage: '',
            paginationButtons:[],
        }
    },
    methods: {
        async getListCategory(currentPage, search){
            try{
                const res = await categoriesApi.getListCategories(this.currentPage,this.name)
                this.category = res.data.listCategories.content
                this.currentPage = res.data.currentPage
                this.totalPage = res.data.listCategories.totalPages
                this.setupPagination(this.totalPage)
            }
            catch(err){
                console.log("err: "+err)
            }
        },
        async search(name){
            console.log("name: "+name)
            await this.getListCategory(this.currentPage, name)
        },
        async addCategory(categoryDto){
            try{
                const res = await categoriesApi.postAddCategories(categoryDto)
                    if(res.success){
                        await this.getListCategory(this.currentPage,"")
                        this.categoryDto = {}
                        let mess='Thêm thành công'
				        this.showToastr(1,mess)
                        bootstrap.Modal.getInstance(document.getElementById("add")).hide()
                    }
                    if(res.err){
                        let mess='Thêm thất bại'
				        this.showToastr(0,mess)
                    }
            }
            catch(err){
                console.log("err: "+err)
            }
        },
        async getEditCategory(id){
            try{
                const res = await categoriesApi.getEditCategories(id)
                this.categoryDto = res.data.categoryDto
            }
            catch(err){
                console.log("err: "+err)
            }
        },
        async clickEditCategory(category){
            try{
                const res = await categoriesApi.postEditCategories(category)
                    if(res.success){
                        await this.getListCategory(this.currentPage,"")
                        let mess='Sửa thành công'
				        this.showToastr(1,mess)
                        bootstrap.Modal.getInstance(document.getElementById("edit"+category.id)).hide()
                    }
                    if(res.err){
                        let mess='Sửa thất bại'
				        this.showToastr(0,mess)
                    }
            }
            catch(err){
                console.log("err: "+err)
            }
        },
        async clickDeleteCategory(id){
            try{
                bootstrap.Modal.getInstance(document.getElementById('delete' + id)).hide()
                const res = await categoriesApi.deleteCategories(id)
                    if(res.success){
                        await this.getListCategory(this.currentPage,"")
                        let mess='Xóa thành công'
				        this.showToastr(1,mess)
                    }
                    if(res.err){
                        let mess='Xóa thất bại'
				        this.showToastr(0,mess)
                    }
            }
            catch(err){
                console.log("err: "+err)
            }
        },
        showToastr(condition,message) {
            if(condition)
				showSuccessToast(message)
			
			if(condition == false)
				showErrorToast(message)
			
        },
        PaginationButton (page) {
			return {
				page,
				isActive: this.currentPage === page,
				handleClick: async () => {
					console.log("page: "+page)
					await this.loadCategory(page);
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
		async loadCategory(page) {
            try{
                const res = await categoriesApi.getListCategories(page,this.name)
                this.category = res.data.listCategories.content
                this.currentPage = res.data.currentPage
                this.totalPage = res.data.listCategories.totalPages
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
            this.getListCategory()
 	},
}
</script>

<style>

</style>