<template>
  <div>
    <head>
        <title>Quản lý người dùng</title>
    </head>
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
						<h1>Quản lý người dùng</h1>
					</div>
					<div class="col-sm-6">
						<ol class="breadcrumb float-sm-right">
							<li class="breadcrumb-item"><a href='/admin/home'>Quản lý</a></li>
							<li class="breadcrumb-item active">Người dùng</li>
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
						<div class="col-6 left px-4">
							<div class="form-group d-flex justify-content-between">
								<label for="inputPassword6" class="col-form-label">Tìm kiếm:</label>
								<input type="text" v-model="search_text" class="form-control" />
							</div>
						</div>
						<div class="col-6 right pl-4">
							<button type="submit" class="btn btn-primary px-4">Tìm kiếm</button>
						</div>
					</div>
				</form>
			</div>
		</section>

		<section class="content">

			<!-- Default box -->
			<div class="card">
				<div class="card-header">
					<h3 class="card-title">Danh sách người dùng</h3>
					<div class="card-tools">
						<a data-bs-toggle="modal" data-bs-target="#add" class="btn btn-primary"><span style="font-size: 18px;">+</span> Thêm mới</a>
					</div>
				</div>
				<div class="card-body">
					<table class="user-table text-center">
						<thead>
							<tr>
								<th>STT</th>
								<th>Tên đăng nhập</th>
								<th>Họ tên</th>
								<th>Email</th>
								<th>Địa chỉ</th>
								<th>Role</th>
								<th>Thao tác</th>
							</tr>
						</thead>
						<tbody>
							<template v-if="user">
									<tr :id="'trow_'+item.id" v-for="(item,index) in user" v-bind:key="item.id">
										<td class="td1" :text="index + ((currentPage - 1) * 3)">{{ index + 1 }}</td>
										<td class="td6"><h6>{{item.username}}</h6></td>
										<td class="td3"><h6>{{ item.name }}</h6></td>
										<td class="td4"><h6>{{item.email}}</h6></td>
										<td class="td7"><h6>{{item.address}}</h6></td>
										<td class="td4"><h6>{{item.role}}</h6></td>
										<td class="td11">
											<a data-bs-toggle="modal" @click="getEditUser(item._id)" :data-bs-target="`#edit`+item._id" class="btn btn-sm btn-primary mr-2"><i class="fa-solid fa-pen-to-square"></i></a> 
											<a data-bs-toggle="modal" :data-bs-target="'#delete'+ item._id" class="btn btn-sm btn-danger"><i class="fa-solid fa-trash"></i></a>
										</td>
										<div class="modal delete-new" :id="'delete'+item._id">
											<div class="modal-dialog">
												<div class="modal-content">
													<div class="modal-header">
														<h4 class="modal-title">Xóa tài khoản</h4>
														<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
													</div>
													<div class="modal-body">
														Bạn có chắc là xóa không ?
													</div>
													<div class="modal-footer">
														<button type="button" class="btn btn-danger" data-bs-dismiss="modal">Hủy</button>
														<button @click="clickDeleteUser(item._id)" class="btn btn-primary">Xác nhận</button>
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
					<form @submit.prevent="addUser(formAddUser)">
						<div class="modal-header">
							<h4 class="modal-title">Thêm tài khoản</h4>
							<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
						</div>
						<div class="modal-body">
							<div id="logins-part" class="content" role="tabpanel" aria-labelledby="logins-part-trigger">
								<div class="form-group">
									<label for="">Họ và tên</label> 
									<input type="text" v-model="formAddUser.name" class="form-control" required="required" />
								</div>
								<div class="form-group"> 
									<label for="">Email</label> 
									<input type="text" v-model="formAddUser.email" class="form-control" required="required" pattern="^\w+([\.-]?\w+)+@\w+([\.-]?\w+)*(\.\w{2,3})+$" title="admin@gmail.com" />
								</div>
								<div class="form-group">
									<label for="">Địa chỉ</label> 
									<input type="text" v-model="formAddUser.address" class="form-control" required="required" />
								</div>
								<div class="form-group">
									<label for="">Tên đăng nhập</label> 
									<input type="text" v-model="formAddUser.username" class="form-control" required="required" />
								</div>
								<div class="form-group">
									<label for="">Mật khẩu</label> 
									<input autocomplete="" type="password" v-model="formAddUser.password" class="form-control" required="required" pattern="^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])([0-9a-zA-Z]{8,})$" title="Ít nhất 8 ký tự trở lên. Có ít nhất một chữ số. Có ít nhất một chữ cái viết thường. Có ít nhất một chữ cái viết hoa." />
								</div>
								<div class="form-group"> 
									<label for="">Role</label> 
									<select class="form-control form-select" v-model="formAddUser.role">
										<option selected="selected" value=""></option>
										<option value="user">USER</option>
										<option value="admin">ADMIN</option>
									</select>
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
		<div v-for="item in user" v-bind:key="item._id" >
			<div class="modal" :id="`edit`+item._id">
				<div class="modal-dialog">
					<div class="modal-content">
						<form id="formEditUser" @submit.prevent="editUser(formEditUser)" enctype="multipart/form-data">
							<div class="modal-header">
								<h4 class="modal-title">Chỉnh sửa tài khoản</h4>
								<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
							</div>
							<div class="modal-body">
								<div id="logins-part" class="content" role="tabpanel" aria-labelledby="logins-part-trigger">
									<div class="form-group">
										<label for="">Id</label> 
										<input type="text" id="idEdit" v-model="formEditUser._id" class="form-control" readonly="readonly"/>
									</div>
									<div class="form-group">
										<label for="">Họ và tên</label> 
										<input type="text" id="fullnameEdit" v-model="formEditUser.name" class="form-control" required="required" />
									</div>
									<div class="form-group">
										<label for="">Địa chỉ</label> 
										<input type="text" class="form-control" id="addressEdit" v-model="formEditUser.address" />
									</div>
									<div class="form-group"> 
										<label for="">Email</label> 
										<input type="text" v-model="formEditUser.email" class="form-control" required="required" pattern="^\w+([\.-]?\w+)+@\w+([\.-]?\w+)*(\.\w{2,3})+$" title="admin@gmail.com" />
									</div>
									<div class="form-group"> 
										<label for="">Role</label> 
										<select class="form-control form-select" v-model="formEditUser.role">
											<option selected="selected" value=""></option>
											<option value="user">USER</option>
											<option value="admin">ADMIN</option>
										</select>
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
  </div>
</template>

<script>
import { showSuccessToast, showErrorToastMess, getGenderDisplay } from "../../../assets/web/js/main";
import userApi from '../../../service/User'
export default {
    data(){
        return {
			user: [],
			currentPage:'',
			totalPage:"",
            search_text: "",
            formAddUser: {},
            formEditUser: {},
			paginationButtons:[],
			imgDto:'',
			showPreload: false
        }
    },
    methods: {
		getGenderDisplay,
		async getListUserAdmin(){
			try{
				const res = await userApi.getListUserAdmin(this.currentPage,this.search_text)
				this.user = res.data
			}catch(err){
				console.log("err: "+err)
			}
		},
		async addUser(formAddUser){
			try{
				this.showPreload = true
				const res = await userApi.addUser(formAddUser)
				if(res.status) showSuccessToast("Thêm mới người dùng thành công")
				if(!res.status) showErrorToastMess("Thêm mới người dùng thất bại")
				this.formAddUser={}
				this.getListUserAdmin();
				this.showPreload = false
				bootstrap.Modal.getInstance(document.getElementById("add")).hide()
			}catch(err){
				this.showPreload = false
				console.log("err: "+err)
				showErrorToastMess("Có lỗi rồi !!")
			}
		},
		async getEditUser(id){
			try{
				const res = await userApi.getEditUser(id)
				this.formEditUser = res
			}catch(err){
				console.log("err: "+err)
			}
		},
		async editUser(formEditUser){
			try{
				this.showPreload = true
				delete formEditUser.username
				const res = await userApi.postEditUser(formEditUser)
				if(res.status){
					this.getListUserAdmin()
					showSuccessToast("Chỉnh sửa người dùng thành công")
				}
				if(!res.status) showErrorToastMess("Chỉnh sửa người dùng thất bại")
				this.showPreload = false
				bootstrap.Modal.getInstance(document.getElementById("edit"+formEditUser._id)).hide()
			}catch(err){
				console.log("err: "+err)
				this.showPreload = false
				showErrorToastMess("Có lỗi rồi !!")
			}
		},
		async clickDeleteUser(id){
			try{
				bootstrap.Modal.getInstance(document.getElementById("delete" + id)).hide()
				const res = await userApi.deleteUser(id)
				if(res.status){
					this.getListUserAdmin()
					showSuccessToast("Xóa thành công")
				}
				if(!res.status) showErrorToastMess("Xóa thất bại")
			}catch(err){
				console.error("err: "+err); showErrorToastMess("Có lỗi xảy ra")
			}
		},

		async search(page,search_text){
			await this.getListUserAdmin(page,search_text)
		},

    },
	mounted(){
		if(!sessionStorage.getItem("login") && sessionStorage.getItem("role")!="admin")
		{
			this.$router.push("/auth/sign-in")
			sessionStorage.setItem("auth",true)
		}
		else
			this.getListUserAdmin()
	}
}
</script>

<style>

</style>