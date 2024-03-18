<template>
<div>
	<head><title>Đặt hàng</title></head>
	<div id="toast">
    </div>
  <section class="order">
			<div class="container">
				<form class="order-form" @submit.prevent="Order()">
					<div class="row">
						<div class="breadcrumbs d-flex flex-row align-items-center col-12">
							<ul>
								<li><a href="/home">Trang chủ</a></li>
								<li class="active"><a href="#"><i
										class="fa fa-angle-right" aria-hidden="true"></i>Đặt hàng</a></li>
							</ul>
						</div>
						<div class="col-lg-6">
							<div class="information-detail">
								<h4>Thông tin đơn hàng</h4>
								<div class="col-12 mb-2 border info-user p-3">
									<div class="col-lg-12 d-flex align-items-center">
										<label>Họ và Tên : </label> <span>{{userLogin.fullname}}</span>
									</div>
									<div class="col-lg-12 d-flex align-items-center">
										<label>Email : </label> <span>{{userLogin.email}}</span>
									</div>
									<div class="col-lg-12 d-flex align-items-center">
										<label>Tổng tiền : </label> <span>{{ formatCurrency(totalMoney) }}</span>
									</div>
									<div class="col-lg-12 d-flex align-items-center">
										<label>Ngày đặt : </label> <span>{{ formatDate(orderDate) }}</span>
									</div>
								</div>
								<div class="col-12  border info-order p-3">
									<div class="col-lg-12  pb-4 ">
										<label>SĐT <span>*</span></label> 
										<input type="text" v-model="OrderRequest.phone" name="phone" required="required" />
									</div>
									<div class="col-lg-12  pb-4">
										<label>Địa chỉ nhận hàng <span>*</span></label> 
										<input type="text" v-model="OrderRequest.address" name="address" required="required" />
									</div>
									<div class="col-lg-12  pb-4">
										<label>Ghi chú </label> 
										<textarea name="note" v-model="OrderRequest.note"  id="floatingTextarea2" class="form-control" style="height: 70px;"></textarea>
									</div>
									<div class="mt-sm-1 ">
										<label class="fw-bold text-size-18 d-block">Vận chuyển <span>*</span></label> 
										<div class="d-flex justify-content-between align-items-center mb-4 ">
											<div class="text-size-14 mt-1">
												<input type="radio" checked style="width: 10px; height: 10px; margin-right: 4px;" />
												<label style="align-items: center;">Giao hàng tận nơi</label>
											</div>
											<span class="fw-bold text-size-14">40.000 đ</span><br>
										</div>
									</div>
									<div class="col-lg-12 ">
										<label>Hình thức thanh toán <span>*</span></label> 
										<select class="form-control form-select" @change="typePAY()" name="typePayment" id="drTypePayment" required="required">
											<option value="COD">Thanh toán khi nhận hàng (COD)</option>
											<option value="TRANSFER">Cổng thanh toán VNPAY</option>
										</select>
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
										<li class="fw-normal" v-for="(item, index) in listCart" :key="index">
												<span><img :src="item.img" style="width:50px; height:50px" alt="Product Image" /></span>
												<span>{{item.amount}}</span>
												<span>{{ formatCurrency(item.price) }}</span>
												<span>{{ item.discount }}%</span>
												<span>{{ formatCurrency(item.totalPrice) }}</span>
										</li>
										<li class="total-price">Tổng số lượng <p>{{totalQuantity}}</p></li>
										<li class="total-price">Tổng tiền <p>{{formatCurrency(totalMoney)}}</p></li>
										<li class="total-price">Phí vận chuyển <p>{{formatCurrency(40000)}}</p></li>
										<li class="total-price">Thành tiền <p>{{ formatCurrency(totalMoney + 40000) }}</p></li>
									</ul>
									<div class="order-btn">
										<button type="submit" class="site-btn place-btn">Đặt hàng</button>
									</div>
								</div>
							</div>
						</div>
					</div>
				</form>
			</div>
		</section>
	</div>
</template>

<script>
import orderApi from '../../../service/Order'
import {showErrorToastMess } from "../../../assets/web/js/main";
import { formatDate, formatCurrency } from "../../../assets/admin/js/format-admin";
export default {
	data(){
		return {
			userLogin: {
				fullname:" ",
				email: ""
			},
			totalMoney: 0,
			totalQuantity:0,
			orderDate: "",
			listCart: [],
			OrderRequest:{
				typePayment: 'COD',
				phone:'',
				address:'',
				bankCode:'' ,
				note:''
			}
		}
	},
	methods: {
		formatDate,
		formatCurrency,
		typePAY(){
			let type = document.getElementById('drTypePayment').value;
			this.OrderRequest.typePayment = type;
			
			// Hiển thị hoặc ẩn phần tử "#load-payment" dựa trên giá trị của "type"
			if (type === "TRANSFER") {
				this.OrderRequest.bankCode = "NCB"
			}
			else
				this.OrderRequest.bankCode = ""

		},
		async getOrder(){
			const res = await orderApi.getOrder()
				this.userLogin.email = res.data.email
				this.userLogin.fullname = res.data.name
				this.listCart = res.data.listCart
				this.orderDate = Date.now()
				for(var item of res.data.listCart){
					this.totalQuantity += item.amount
					this.totalMoney += item.totalPrice
				}
		},
		async Order(){
			const res = await orderApi.postOrder(this.OrderRequest)
			if(res.status == 200){
				sessionStorage.setItem("orderId",res.data.order_id)
				this.$router.push("/bill")
			}
			else
				showErrorToastMess('Có lỗi xảy ra, vui lòng thử lại sau')
		}
	},
	mounted(){
		if (sessionStorage.getItem("login"))
		{
			this.getOrder()
		}
		else
		{
			window.location.href = '/auth/sign-in'
			sessionStorage.setItem("err", true)
		}
	}
}
</script>

<style>

</style>