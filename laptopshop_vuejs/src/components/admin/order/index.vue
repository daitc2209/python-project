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
							<p class="mb-2 pb-1"><strong>{{ orderStatus.order_pending + orderStatus.order_confirm + orderStatus.order_delivery + orderStatus.order_received + orderStatus.order_cancelled }}</strong> Đơn</p>
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
							<p class="mb-2 pb-1"><strong>{{ orderStatus.order_confirm }}</strong> Đơn</p>
						</div>
					</div>
					<div class="card-item">
						<div class="card-circle delivering">
							<i class="card-icon delivering fa-solid fa-truck-fast"></i>
						</div>
						<div class="card-status">
							<h4 class="card-label">Đang vận chuyển</h4>
							<p class="mb-2 pb-1"><strong>{{ orderStatus.order_delivery }}</strong> Đơn</p>
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
					<div class="order-range">
						<div class="order-search">
							<i class="fas fa-search"></i>
							<input type="text" class="order-search__input" v-model="search_text" placeholder="Tên, Mã đơn hàng">
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
									<tr :id="'trow_'+item._id" v-for="(item,index) in order" :key="item._id">
										<td class="td1" :text="index + ((currentPage - 1) * 3)">{{ index + 1 }}</td>
										<td class="td2"><h6>{{item.name}}</h6></td>
										<td class="td3"><h6>{{formatDate(item.createdAt)}}</h6></td>
										<td class="td4"><h6>{{formatCurrency(item.total_money)}}</h6></td>
										<td class="td5"><h6>COD</h6></td>
										<td class="td6"><h6>{{getStateCheckoutDisplay(item.state_checkout)}}</h6></td> 
										<td class="td7"><h6>{{getStateOrderDisplay(item.state_order)}}</h6></td>
										<td class="td8">
											<a data-bs-toggle="modal" :data-bs-target="'#see'+item._id" class="btn btn-sm btn-primary mr-2"><i class="fa-solid fa-eye"></i></a> 
											<a v-if="item.state_order == 4 || item.state_order == 3" class="btn btn-sm btn-secondary">Status</a>
											<a v-if="item.state_order != 4 && item.state_order != 3" data-bs-toggle="modal" :data-bs-target="'#vertify'+item._id" @click="getOrder(item._id)" class="btn btn-sm btn-danger">Status</a>
										</td>
										<div class="modal see-order" :id="'see'+item._id">
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
																							<label>Mã đơn hàng :</label> <label>#{{item.code_order}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>OrderId :</label> <label>#{{item._id}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>UserId :</label> <label>#{{item.user_id}}</label>
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
																							<label>Ngày đặt :</label> <label>{{formatDate(item.createdAt)}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>Số lượng sản phẩm :</label><label>{{item.amount}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>Tổng tiền :</label> <label>{{formatCurrency(item.total_money)}}</label>
																						</div>
																						<div class="col-lg-12 d-flex align-items-center">
																							<label>Hình thức thanh toán :</label> <label>COD</label>
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
																							<li><span>Sản phẩm</span><span>Số lượng</span><span>Giá</span><span>Discount</span><span>Tổng</span></li>
																							<span v-for="items in item.orderdetail" :key="items._id">
																								<li class="fw-normal">
																								<span><img :src="items.img" width="50px" height="50px" />{{items.name}}</span> 
																								<span>{{items.amount}}</span>
																								<span>{{ formatCurrency(items.price) }}</span>
																								<span>{{ items.discount }}%</span> 
																								<span>{{formatCurrency(items.total)}}</span></li>
																							</span>
																							<li class="total-price">Tổng số lượng <p>{{item.amount}}</p></li>
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

										<div class="modal" :id="'vertify'+item._id">
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
																	<input type="text" v-model="orderDto._id" class="form-control" readonly="readonly" />
																</div>
																<div class="form-group">
																	<label for="">Trạng thái</label> 
																	<select name="status" v-model="orderDto.state_order" class="form-control form-select" required="required">
																		<option hidden="" :value="orderDto.state_order">{{getStateOrderDisplay(orderDto.state_order)}}</option>
																		<option title="Chờ xác nhận" value="0">Chờ xác nhận</option>
																		<option title="Đã xác nhận" value="1">Đã xác nhận</option>
																		<option title="Đang vận chuyển" value="2">Đang vận chuyển</option>
																		<option title="Đã nhận" value="3">Đã nhận</option>
																		<option title="Đã hủy" value="4">Đã hủy</option>
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
			</div>
		</section>
  </div>
</template>

<script>
import orderApi from '../../../service/Order';
import { showSuccessToast, showErrorToastMess, getStateCheckoutDisplay, getStateOrderDisplay } from "../../../assets/web/js/main";
import { formatDate, formatCurrency } from "../../../assets/admin/js/format-admin";
export default {
    data(){
        return {
			order: [],
            search_text: '',
			startDate: null,
			endDate: null,
			status: 5,
			currentPage:'',
			totalPage:'',
			paginationButtons:[],
			orderDto:{},
			orderStatus:{
				order_cancelled:0,
				order_received:0,
				order_delivery:0,
				order_confirm:0,
				order_pending:0
			},
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
				this.orderStatus = res;
			}catch(err){
				console.log("err: "+err)
				showErrorToastMess("Lỗi lấy đơn hàng theo trạng thái")
			}
		},

		async getOrderByStatus(data){
			try{
				const res = await orderApi.getListOrderByStatus(this.search_text,data)
					this.order = res.data
			}catch(err){
				this.order = false
			}
			
			await this.getAllOrderByStatus()
		},
		async getOrder(id){
			try{
				const res = await orderApi.getOrderById(id)
				if(res) this.orderDto = res.order;
			}catch(err){
				showErrorToastMess("Lấy đơn hàng thất bại")
			}
		},
        async clickVerifyOrder(item){
			try{
				this.showPreload = true
				const res = await orderApi.verify(item._id,item.state_order)
				if(res.status)
				{
					showSuccessToast("Đổi trạng thái thành công")
					this.getOrderByStatus(this.status)
				}
				if(!res.status)
					showErrorToastMess("Đổi trạng thái thất bại")
				this.showPreload = false
				bootstrap.Modal.getInstance(document.getElementById("vertify"+item._id)).hide()
			}catch(err){
				this.showPreload = false
				console.log("err: "+err)
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
		if(!sessionStorage.getItem("login") && sessionStorage.getItem("role")!="admin")
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