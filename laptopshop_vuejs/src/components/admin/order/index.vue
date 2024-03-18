<template>
  <div>
    <head>
        <title>Quản lý đơn hàng</title>
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
						<h1>Quản lý đơn hàng</h1>
					</div>
					<div class="col-sm-6">
						<ol class="breadcrumb float-sm-right">
							<li class="breadcrumb-item"><a href='/admin/home'>Quản lý</a></li>
							<li class="breadcrumb-item active">Đơn hàng</li>
						</ol>
					</div>
				</div>
			</div>
		</section>
		<section class="search">
			<div id="toast">
    		</div>
				<div class="card-container container">
					<div class="card-item">
						<div class="card-circle">
							<i class="card-icon fa-solid fa-clipboard"></i>
						</div>
						<div class="card-status">
							<h4 class="card-label">Tất cả đơn</h4>
							<p class="mb-2 pb-1"><strong>{{ orderStatus.order_pending + orderStatus.order_confirmed + orderStatus.order_delivering + orderStatus.order_received + orderStatus.order_cancelled }}</strong> Đơn</p>
						</div>
					</div>
					<div class="card-item">
						<div class="card-circle pending">
							<i class="card-icon pending fa-solid fa-bell"></i>
						</div>
						<div class="card-status">
							<h4 class="card-label">Chờ xác nhận</h4>
							<p class="mb-2 pb-1"><strong>{{ orderStatus.order_pending }}</strong> Đơn</p>
						</div>
					</div>
					<div class="card-item">
						<div class="card-circle confirmed">
							<i class="card-icon confirmed fa-solid fa-clock"></i>
						</div>
						<div class="card-status">
							<h4 class="card-label">Đã xác nhận</h4>
							<p class="mb-2 pb-1"><strong>{{ orderStatus.order_confirmed }}</strong> Đơn</p>
						</div>
					</div>
					<div class="card-item">
						<div class="card-circle delivering">
							<i class="card-icon delivering fa-solid fa-truck-fast"></i>
						</div>
						<div class="card-status">
							<h4 class="card-label">Đang vận chuyển</h4>
							<p class="mb-2 pb-1"><strong>{{ orderStatus.order_delivering }}</strong> Đơn</p>
						</div>
					</div>
					<div class="card-item">
						<div class="card-circle received">
							<i class="card-icon received fa-solid fa-circle-check"></i>
						</div>
						<div class="card-status">
							<h4 class="card-label">Đã giao</h4>
							<p class="mb-2 pb-1"><strong>{{ orderStatus.order_received }}</strong> Đơn</p>
						</div>
					</div>
					<div class="card-item">
						<div class="card-circle cancelled">
							<i class="card-icon cancelled fa-solid fa-circle-xmark"></i>
						</div>
						<div class="card-status">
							<h4 class="card-label">Đã hủy</h4>
							<p class="mb-2 pb-1"><strong>{{ orderStatus.order_cancelled }}</strong> Đơn</p>
						</div>
					</div>
				</div>
		</section>

		<section class="content">
			<div class="card">
				<div class="card-header">
					<h3 class="card-title" style="padding-bottom: 10px;">Trạng thái đơn hàng</h3>
					<div class="order-container__status">
						<div class="order-status">
							<button @click="getOrderByStatus('all')" id="btn-all" class="order-status__item active">Tất cả</button>
							<button @click="getOrderByStatus('pending')" id="btn-pending" class="order-status__item">Chờ xác nhận</button>
							<button @click="getOrderByStatus('confirmed')" id="btn-confirmed" class="order-status__item">Đã xác nhận</button>
							<button @click="getOrderByStatus('delivering')" id="btn-delivering" class="order-status__item">Đang vận chuyển</button>
							<button @click="getOrderByStatus('received')" id="btn-received" class="order-status__item">Đã giao</button>
							<button @click="getOrderByStatus('cancelled')" id="btn-cancelled" class="order-status__item">Đã hủy</button>
						</div>
					</div>
					
					<div class="order-range">
						<div class="order-search">
							<i class="fas fa-search"></i>
							<input type="text" class="order-search__input" v-model="search_text" placeholder="Tên/ Mã đơn hàng/ Hình thức thanh toán">
						</div>
						<div>
							<div class="order-date">
								<label class="order-range__from" for="startDate">Từ </label>
								<div class="date-picker">
									<VueDatePicker v-model="startDate" format="yyyy-MM-dd"></VueDatePicker>
								</div>
							</div>
							<div class="order-date">
								<label class="order-range__from" for="endDate">Đến </label>
								<VueDatePicker v-model="endDate" format="yyyy-MM-dd"></VueDatePicker>
							</div>
							<button class="order-range__btn btn btn-primary" @click="search()">Tìm kiếm</button>
						</div>
					</div> 
				</div>
				<div class="card-body">
					<table class="order-table">
						<thead>
							<tr>
								<th>No.</th>
								<th>Tên người đặt</th>
								<th>Ngày đặt</th>
								<th>Tổng tiền</th>
								<th>Hình thức thanh toán</th>
								<th>Thanh toán</th>
								<th>Trạng thái</th>
								<th>Thao tác</th>
							</tr>
						</thead>
						<tbody>
							<template v-if="order"> 	
									<tr :id="'trow_'+item.id" v-for="(item,index) in order" :key="item.id">
										<td class="td1" :text="index + ((currentPage - 1) * 3)">{{ index + 1 }}</td>
										<td class="td2"><h6>{{item.name}}</h6></td>
										<td class="td3"><h6>{{formatDate(item.created_at)}}</h6></td>
										<td class="td4"><h6>{{formatCurrency(item.total_money)}}</h6></td>
										<td class="td5"><h6>{{item.payment}}</h6></td>
										<td class="td6"><h6>{{getStateCheckoutDisplay(item.stateCheckout)}}</h6></td> 
										<td class="td7"><h6>{{getStateOrderDisplay(item.stateOrder)}}</h6></td>
										<td class="td8">
											<a data-bs-toggle="modal" :data-bs-target="'#see'+item.id" class="btn btn-sm btn-primary mr-2"><i class="fa-solid fa-eye"></i></a> 
											<a v-if="item.stateOrder == 'CANCELLED' || item.stateOrder == 'RECEIVED'" class="btn btn-sm btn-secondary">Status</a>
											<a v-if="item.stateOrder != 'CANCELLED' && item.stateOrder != 'RECEIVED'" data-bs-toggle="modal" :data-bs-target="'#vertify'+item.id" @click="getOrder(item.id)" class="btn btn-sm btn-danger">Status</a>
										</td>
										<div class="modal see-order" :id="'see'+item.id">
											<div class="modal-dialog">
												<div class="modal-content">
														<div class="modal-header">
															<h4 class="modal-title">Chi tiết đơn hàng</h4>
															<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
														</div>
														<div class="modal-body p-0">
															<section class="order p-0">
																<div class="container">
																	<div class="order-form">
																		<div class="row">
																			<div class="col-lg-6">
																				<div class="information-detail">
																					<h4>Thông tin đơn hàng</h4>
																					<div class="col-12 mb-2 border info-user p-3">
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>Mã đơn hàng :</label> <label>#{{item.codeOrder}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>OrderId :</label> <label>#{{item.id}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>UserId :</label> <label>#{{item.user}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>Họ và tên :</label> <label>{{item.name}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>Email :</label> <label>{{item.email}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>SĐT :</label> <label>{{item.phone}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>Địa chỉ nhận hàng :</label> <label>{{item.address_delivery}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>Ngày đặt :</label> <label>{{formatDate(item.created_at)}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>Số lượng sản phẩm :</label><label>{{item.num}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>Tổng tiền :</label> <label>{{formatCurrency(item.total_money)}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>Hình thức thanh toán :</label> <label>{{item.payment}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>Ghi chú :</label> <label>{{item.note}}</label>
																						</div>
																					</div>
																				</div>
																			</div>
																			<div class="col-lg-6">
																				<div class="place-order">
																					<h4>Thông tin sản phẩm</h4>
																					<div class="order-total">
																						<ul class="order-table p-0">
																							<li><span>id</span><span>Sản phẩm</span><span>Số lượng</span><span>Giá</span><span>Discount</span><span>Tổng</span></li>
																							<span v-for="items in item.orderdetail" :key="items.id">
																								<li class="fw-normal"><span>#{{items.product.id}}</span>
																								<span><img :src="items.product.img" width="50px" height="50px" />{{items.product.name}}</span> 
																								<span>{{items.num}}</span>
																								<span>{{ formatCurrency(items.product.price) }}</span>
																								<span>{{ items.product.discount }}%</span> 
																								<span>{{formatCurrency(items.totalPrice)}}</span></li>
																							</span>
																							<li class="total-price">Tổng số lượng <p>{{item.num}}</p></li>
																							<li class="total-price">Tổng tiền <p>{{formatCurrency(item.total_money-40000)}}</p></li>
																							<li class="total-price">Phí vận chuyển <p>{{formatCurrency(40000)}}</p></li>
																							<li class="total-price">Thành tiền <p>{{formatCurrency(item.total_money)}}</p></li>
																						</ul>
																					</div>
																				</div>
																			</div>
																		</div>
																	</div>
																</div>
															</section>
														</div>
														<div class="modal-footer">
															<button type="button" class="btn btn-danger" data-bs-dismiss="modal">Đóng</button>
														</div>
												</div>
											</div>
										</div>

										<div class="modal" :id="'vertify'+item.id">
											<div class="modal-dialog">
												<div class="modal-content">
													<form @submit.prevent="clickVerifyOrder(orderDto)" >
														<div class="modal-header">
															<h4 class="modal-title">Cập nhật trạng thái đơn hàng</h4>
															<button type="button" class="btn-close" data-bs-dismiss="modal"></button>
														</div>

														<div class="modal-body">
															<div id="logins-part" class="content" role="tabpanel" aria-labelledby="logins-part-trigger">
																<div class="form-group">
																	<label for="">Id</label> 
																	<input type="text" v-model="orderDto.id" class="form-control" readonly="readonly" />
																</div>
																<div class="form-group">
																	<label for="">Trạng thái</label> 
																	<select name="status" v-model="orderDto.stateOrder" class="form-control form-select" required="required">
																		<option hidden="" :value="orderDto.stateOrder">{{orderDto.stateOrder}}</option>
																		<option value="CONFIRMED">CONFIRMED</option>
																		<option value="DELIVERING">DELIVERING</option>
																		<option value="RECEIVED">RECEIVED</option>
																		<option value="CANCELLED">CANCELLED</option>
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
				<template v-if="order">
					<div class="pagination" id="pagination" v-if="paginationButtons.length >= 2">
						<button v-for="page in paginationButtons" :key="page" 
						:class="{ active: currentPage === page }" 
						@click="PaginationButton(page).handleClick()">
							{{ page }}
						</button>
					</div>
				</template>
			</div>
		</section>
  </div>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import orderApi from '../../../service/Order';
import { showSuccessToast, showErrorToastMess, getStateCheckoutDisplay, getStateOrderDisplay } from "../../../assets/web/js/main";
import { formatDate, formatCurrency } from "../../../assets/admin/js/format-admin";
export default {
	components: {
		VueDatePicker
    },
    data(){
        return {
			order: [],
            search_text: '',
			startDate: null,
			endDate: null,
			status:'all',
			currentPage:'',
			totalPage:'',
			paginationButtons:[],
			orderDto:{},
			orderStatus:{},
			showPreload: false
        }
    },
    methods: {
		formatDate,
		formatCurrency,
		getStateCheckoutDisplay,
		getStateOrderDisplay,
		async getAllOrderByStatus(){
			try{
				const res = await orderApi.getAllOrderByStatus()
				this.orderStatus = res.data;
			}catch(err){
				console.log("err: "+err)
				showErrorToastMess("Lỗi lấy đơn hàng theo trạng thái")
			}
		},

		async getOrderByStatus(data){
			var buttons = document.getElementsByClassName('order-status__item');
			for (var i = 0; i < buttons.length; i++) {
				buttons[i].classList.remove('active');
			} 
			var selectedButton = document.getElementById('btn-' + data);
				selectedButton.classList.add('active');

			//Kiểm tra xem trạng thái đơn hàng có thay đổi không, nếu có thì đặt lại page
			this.currentPage = this.status !== data ? 1 : this.currentPage;
			this.status = data

			if(this.startDate !== null || this.endDate !== null)
				await this.search()
			
			else{
				try{
					const res = await orderApi.getListOrderByStatus(this.currentPage,this.search_text,this.status)
						this.order = res.data.listOrders
						this.totalPage = res.data.totalPage
						this.currentPage = res.data.currentPage
						this.setupPagination(this.totalPage)
				}catch(err){
					this.order = false
				}
			}
			await this.getAllOrderByStatus()
		},
		async getOrder(id){
			try{
				const res = await orderApi.getOrderById(id)
				if(res) this.orderDto = res.data.orders;
			}catch(err){
				showErrorToastMess("Lấy đơn hàng thất bại")
			}
		},
        async clickVerifyOrder(item){
			try{
				this.showPreload = true
				const res = await orderApi.verify(item.id,item.stateOrder)
				if(res.message)
				{
					showSuccessToast("Đổi trạng thái thành công")
					this.getOrderByStatus(this.status)
				}
				if(res.error)
					showErrorToastMess("Đổi trạng thái thất bại")
				this.showPreload = false
				bootstrap.Modal.getInstance(document.getElementById("vertify"+item.id)).hide()
			}catch(err){
				this.showPreload = false
				console.log("err: "+err)
			}
		},
		async search(){
			try{
				let start = null
				let end = null
				if(this.startDate !== null || this.endDate !== null)
				{
					start = this.formatDate(this.startDate)
					end = this.formatDate(this.endDate)
				}
				let status = this.status
				let search_text = this.search_text
				let data = {search_text,start,end,status}
				if (start > end) {
					let error = 'Ngày bắt đầu không được lớn hơn ngày kết thúc.';
					showErrorToastMess(error)
				} else {
					const res = await orderApi.findByRangeDay(1,data)
					if(res)
					{
						this.order = res.data.listOrders
						this.totalPage = res.data.totalPage
						this.currentPage = res.data.currentPage
						this.setupPagination(this.totalPage)
					}
				}
			}
			catch(err){console.log("err: "+err)}
		},
        PaginationButton (page) {
			return {
				page,
				isActive: this.currentPage === page,
				handleClick: async () => {
					await this.loadOrders(page,this.search_text,this.status);
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
		async loadOrders(page, search_text, status) {
			if(this.startDate !== null || this.endDate !== null){
				let start = this.formatDate(this.startDate)
				let end = this.formatDate(this.endDate)
				let data = {search_text,start,end,status}
				if (start > end) {
					let error = 'Ngày bắt đầu không được lớn hơn ngày kết thúc.';
					showErrorToastMess(error)
				} else {
					try{
						const res = await orderApi.findByRangeDay(page,data)
						if(res)
						{
							this.order = res.data.listOrders
							this.totalPage = res.data.totalPage
							this.currentPage = res.data.currentPage
						}
					}catch(err){
						console.log("err: "+err)
					}
				}
			}
			else{
				try{
					const res = await orderApi.getListOrderByStatus(page,search_text,status)
						this.order = res.data.listOrders
						this.totalPage = res.data.totalPage
						this.currentPage = res.data.currentPage
				}catch(err){
					this.order = false
				}
			}
    	},
		init(){
			this.getAllOrderByStatus();
			this.getOrderByStatus(this.status)
		}
    },
	watch: {
		async search_text () {
			await this.getOrderByStatus(this.status);
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
@import url('../../../assets/admin/css/order.css');
</style>