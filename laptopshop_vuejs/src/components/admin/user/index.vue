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
				<form @submit.prevent="search(1,formSearchUser)">
					<div class="row">
						<div class="col-6 left px-4">
							<div class="form-group d-flex justify-content-between">
								<label for="inputPassword6" class="col-form-label">Họ và tên:</label>
								<input type="text" v-model="formSearchUser.fullname" class="form-control" />
							</div>
							<div class="form-group d-flex justify-content-between">
								<label for="inputPassword6" class="col-form-label">Giới tính:</label>
								<select class="form-control form-select" v-model="formSearchUser.sex">
									<option selected="selected" value=""></option>
									<option value="MALE">Nam</option>
									<option value="FEMALE">Nữ</option>
								</select>
							</div>
							<div class="form-group d-flex justify-content-between">
								<label for="inputPassword6" class="col-form-label">Địa chỉ:</label>
								<input type="text" v-model="formSearchUser.address" class="form-control" />
							</div>
						</div>
						<div class="col-6 right px-4">
							<div class="form-group d-flex justify-content-between">
								<label for="inputPassword6" class="col-form-label">Email:</label>
								<input type="text" v-model="formSearchUser.email" class="form-control" />
							</div>
							<div class="form-group d-flex justify-content-between">
								<label for="inputPassword6" class="col-form-label">Trạng thái:</label>
								<select class="form-control form-select" v-model="formSearchUser.stateUser">
									<option selected="selected" value=""></option>
									<option value="PENDING">PENDING</option>
									<option value="ACTIVED">ACTIVED</option>
									<option value="DISABLED">DISABLED</option>
									<option value="REMOVED">REMOVED</option>
								</select>
							</div>
							<div class="form-group d-flex justify-content-between">
								<label for="inputPassword6" class="col-form-label">AuthType:</label>
								<select class="form-control form-select" v-model="formSearchUser.authType">
									<option selected="selected" value=""></option>
									<option value="DATABASE">DATABASE</option>
									<option value="GOOGLE">GOOGLE</option>
									<option value="FACEBOOK">FACEBOOK</option>
								</select>
							</div>
						</div>
						<div class="d-flex justify-content-center pr-4 mb-3">
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
								<th>Img</th>
								<th>Họ tên</th>
								<th>Email</th>
								<th>SĐT</th>
								<th>Giới tính</th>
								<th>Ngày sinh</th>
								<th>Địa chỉ</th>
								<th>Trạng thái</th>
								<th>Auth Type</th>
								<th>Thao tác</th>
							</tr>
						</thead>
						<tbody>
							<template v-if="user">
									<tr :id="'trow_'+item.id" v-for="(item,index) in user" v-bind:key="item.id">
										<td class="td1" :text="index + ((currentPage - 1) * 3)">{{ index + 1 }}</td>
										<td class="td2"><img :src='item.img' alt=""></td>
										<td class="td3"><h6>{{ item.fullname }}</h6></td>
										<td class="td4"><h6>{{item.email}}</h6></td>
										<td class="td4"><h6>{{item.phone}}</h6></td>
										<td class="td5"><h6>{{getGenderDisplay(item.gender)}}</h6></td>
										<td class="td6"><h6>{{item.dob}}</h6></td>
										<td class="td7"><h6>{{item.address}}</h6></td>
										<td class="td8"><h6>{{item.stateUser}}</h6></td>
										<td class="td9"><h6>{{item.authType}}</h6></td>
										<td class="td11">
											<a v-if="item.stateUser == `ACTIVED`" data-bs-toggle="modal" :data-bs-target="'#lock'+ item.id" class="btn btn-sm btn-confirmed mr-2"><i class="fa-solid fa-lock-open"></i></a>
											<a v-else data-bs-toggle="modal" :data-bs-target="'#unlock'+ item.id" class="btn btn-sm btn-secondary mr-2"><i class="fa-solid fa-lock"></i></a>
											<a data-bs-toggle="modal" @click="getEditUser(item.id)" :data-bs-target="`#edit`+item.id" class="btn btn-sm btn-primary mr-2"><i class="fa-solid fa-pen-to-square"></i></a> 
											<a data-bs-toggle="modal" :data-bs-target="'#delete'+ item.id" class="btn btn-sm btn-danger"><i class="fa-solid fa-trash"></i></a>
										</td>
										<div class="modal delete-new" :id="'delete'+item.id">
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
														<button @click="clickDeleteUser(item.id)" class="btn btn-primary">Xác nhận</button>
													</div>
												</div>
											</div>
										</div>
										<div class="modal lock-new" :id="'lock'+item.id">
											<div class="modal-dialog">
												<div class="modal-content">
													<div class="modal-header">
														<h4 class="modal-title">Khóa tài khoản</h4>
														<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
													</div>
													<div class="modal-body">
														Bạn có chắc là khóa tài khoản này không ?
													</div>
													<div class="modal-footer">
														<button type="button" class="btn btn-danger" data-bs-dismiss="modal">Hủy</button>
														<button @click="clicklockUser(item.id)" class="btn btn-primary">Xác nhận</button>
													</div>
												</div>
											</div>
										</div>
										<div class="modal unlock-new" :id="'unlock'+item.id">
											<div class="modal-dialog">
												<div class="modal-content">
													<div class="modal-header">
														<h4 class="modal-title">Mở tài khoản</h4>
														<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
													</div>
													<div class="modal-body">
														Bạn có chắc là mở tài khoản này không ?
													</div>
													<div class="modal-footer">
														<button type="button" class="btn btn-danger" data-bs-dismiss="modal">Hủy</button>
														<button @click="clickUnlockUser(item.id)" class="btn btn-primary">Xác nhận</button>
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
									<input type="text" v-model="formAddUser.fullname" class="form-control" required="required" />
								</div>
								<div class="form-group"> 
									<label for="">Email</label> 
									<input type="text" v-model="formAddUser.email" class="form-control" required="required" pattern="^\w+([\.-]?\w+)+@\w+([\.-]?\w+)*(\.\w{2,3})+$" title="admin@gmail.com" />
								</div>
								<div class="form-group">
									<label for="">Tên đăng nhập</label> 
									<input type="text" v-model="formAddUser.username" class="form-control" required="required" />
								</div>
								<div class="form-group">
									<label for="">Mật khẩu</label> 
									<input autocomplete="" type="password" v-model="formAddUser.password" class="form-control" required="required" pattern="^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])([0-9a-zA-Z]{8,})$" title="Ít nhất 8 ký tự trở lên. Có ít nhất một chữ số. Có ít nhất một chữ cái viết thường. Có ít nhất một chữ cái viết hoa." />
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
		<div v-for="item in user" v-bind:key="item.id" >
			<div class="modal" :id="`edit`+item.id">
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
										<input type="text" id="idEdit" v-model="formEditUser.id" class="form-control" readonly="readonly"/>
									</div>
									<div class="form-group">
										<label for="">Họ và tên</label> 
										<input type="text" id="fullnameEdit" v-model="formEditUser.fullname" class="form-control" required="required" />
									</div>
									<div class="form-group">
										<label for="">Giới tính</label> 
										<select class="form-control form-select" id="sexEdit" v-model="formEditUser.gender" >
											<option value="MALE">Nam</option>
											<option value="FEMALE">Nữ</option>
										</select>
									</div>
									<div class="form-group">
										<label for="">Ngày sinh</label> 
										<input type="text" class="form-control" id="birthdayEdit" v-model="formEditUser.dob" placeholder="yyyy-mm-dd" pattern="^\d{4}-\d{2}-\d{2}$" title="Định dạng: yyyy-mm-dd" />
									</div>
									<div class="form-group">
										<label for="">Địa chỉ</label> 
										<input type="text" class="form-control" id="addressEdit" v-model="formEditUser.address" />
									</div>
									<div class="form-group">
										<label for="">SĐT</label> 
										<input type="text" class="form-control" id="phoneEdit" v-model="formEditUser.phone" pattern="^\d+$" title="Vui lòng chỉ nhập số" />
									</div>
									<div class="form-group">
										<label for="">Trạng thái</label> 
										<select class="form-control form-select" id="stateUserEdit" v-model="formEditUser.stateUser" required="required">
											<option value="PENDING">PENDING</option>
											<option value="ACTIVED">ACTIVED</option>
											<option value="DISABLED">DISABLED</option>
											<option value="REMOVED">REMOVED</option>
										</select>
									</div>
									<div class="form-group">
										<label for="">Img</label> 
										<input hidden="" type="text" v-model="formEditUser.img" id="imgEdit" /> 
										<input class="form-control" @change="chooseFile" type="file" id="fileImage" name="fileImage" 
										ref="file"
										accept=".png, .jpg, jpeg"
										:maxFileSize="1000000" />
									</div>
									<div class="form-group d-flex justify-content-center">
										<img id="imageEdit" class="imgEdit" :src="formEditUser.img" style="height: 200px; width: 200px"/>
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
            formSearchUser: {},
            formAddUser: {role:2},
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
				const res = await userApi.getListUserAdmin(this.currentPage,
					this.formSearchUser.fullname,
					this.formSearchUser.sex,
					this.formSearchUser.address,
					this.formSearchUser.email,
					this.formSearchUser.stateUser,
					this.formSearchUser.authType)
					this.user = res.data.listUser.content
				this.totalPage = res.data.listUser.totalPages
				this.currentPage = res.data.currentPage
				this.setupPagination(this.totalPage)
			}catch(err){
				console.log("err: "+err)
			}
		},
		async addUser(formAddUser){
			try{
				this.showPreload = true
				const res = await userApi.addUser(formAddUser)
				if(res.success) showSuccessToast("Thêm mới người dùng thành công")
				if(res.error) showErrorToastMess("Thêm mới người dùng thất bại")
				this.formAddUser={role:2}
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
				const formData = new FormData();
				if(this.imgDto != "" && this.imgDto != null)
					formEditUser.img = this.imgDto
				formData.append('fileImage', formEditUser.img);
				formData.append('id', formEditUser.id);
				formData.append('fullname', formEditUser.fullname);
				formData.append('address', formEditUser.address);
				formData.append('sex', formEditUser.gender);
				formData.append('birthday', formEditUser.dob);
				formData.append('stateUser', formEditUser.stateUser);
				formData.append('phone', formEditUser.phone);
				const res = await userApi.postEditUser(formData)
				if(res.success){
					this.getListUserAdmin()
					showSuccessToast("Chỉnh sửa người dùng thành công")
				}
				if(res.error) showErrorToastMess("Chỉnh sửa người dùng thất bại")
				this.showPreload = false
				bootstrap.Modal.getInstance(document.getElementById("edit"+formEditUser.id)).hide()
			}catch(err){
				console.log("err: "+err)
				this.showPreload = false
				showErrorToastMess("Có lỗi rồi !!")
			}
		},
        async clicklockUser(id){
			try{
				bootstrap.Modal.getInstance(document.getElementById("lock"+id)).hide()
				const res = await userApi.lockUser(id)
				if(res.success){
					this.getListUserAdmin()
					showSuccessToast("Khóa người dùng thành công")
				}
				if(res.error) showErrorToastMess("Khóa người dùng thất bại")
				
			}catch(err){
				console.error("err: "+error);
			}
		},
        async clickUnlockUser(id){
			try{
				bootstrap.Modal.getInstance(document.getElementById("unlock"+id)).hide()
				const res = await userApi.unlockUser(id)
				if(res.success){
					this.getListUserAdmin()
					showSuccessToast("Mở khóa người dùng thành công")
				}
				if(res.error) showErrorToastMess("Mở khóa người dùng thất bại")
			}catch(err){
				console.error("err: "+error); showErrorToastMess("Có lỗi xảy ra")
			}
		},
		async clickDeleteUser(id){
			try{
				bootstrap.Modal.getInstance(document.getElementById("delete" + id)).hide()
				const res = await userApi.deleteUser(id)
				if(res.success){
					this.getListUserAdmin()
					showSuccessToast("Xóa thành công")
				}
				if(res.error) showErrorToastMess("Xóa thất bại")
			}catch(err){
				console.error("err: "+error); showErrorToastMess("Có lỗi xảy ra")
			}
		},

		async search(page,formSearchUser){
			await this.getListUserAdmin(page,formSearchUser.fullname,
				formSearchUser.sex,
				formSearchUser.address,
				formSearchUser.email,
				formSearchUser.stateUser,
				formSearchUser.authType)
		},

		chooseFile(e){
			const file = e.target.files[0];
			if (file) {
				this.imgDto = file;
				this.formEditUser.img = URL.createObjectURL(file)
				this.formEditUser.urlImg = true
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
					await this.loadUsers(page);
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
		async loadUsers(page) {
			try{
				const res = await userApi.getListUserAdmin(page)
				this.user = res.data.listUser.content
					this.totalPage = res.data.listUser.totalPages
					this.currentPage = res.data.currentPage
			}catch(err){console.log("err: "+err)}
    	},
    },
	mounted(){
		if(!sessionStorage.getItem("login") && sessionStorage.getItem("role")!="ROLE_ADMIN")
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