<template>
  <div>
    <head><title>Trang giỏ hàng</title></head>
    <div class="breadcrumbs d-flex flex-row align-items-center col-12 container  mt-2">
			<ul class="m-0">
				<li><a href="/home">Trang chủ</a></li>
				<li class="active"><a href="#"><i class="fa fa-angle-right" aria-hidden="true"></i>Giỏ hàng</a></li>
			</ul>
		</div>
		
    	<section class="shopping-cart ">
			<div class="container">
				<div class="row">
					<div class="col-lg-12">
						<div class="cart-table">
							<table>
								<thead>
									<tr>
										<th></th>
										<th>Tên sản phẩm</th>
										<th>Giá</th>
										<th>Số lượng</th>
										<th>Giảm giá</th>
										<th>Tổng</th>
										<th></th>
									</tr>
								</thead>
								<tbody>
									<template v-if="listCart && listCart != '' && listCart != null">
										<tr v-for="item in listCart" :key="item._id">
											<td class="cart-pic first-row"><img :src="item.img" alt=""></td>
											<td class="cart-title first-row"><router-link class="cart-title_name" :to="`/store/${item.product_id}`"><h5>{{item.name}}</h5></router-link></td>
											<td class="p-price first-row"><h5>{{ formatCurrency(item.price) }}</h5></td>
											<td class="qua-col first-row">
												<div class="quantity">
													<div class="pro-qty">
														<a @click=" item.amount > 1 ? decreaseQty(item) : null" ><span class="dec qtybtn" :class="{ disabled: item.amount <= 1 }">-</span> </a>
														<input class="id-1" type="text" :value="item.amount" readonly="readonly"> 
														<a @click="item.amount < item.quantity_in_stock ? increaseQty(item) : null"><span  class="inc qtybtn">+</span></a>
													</div>
												</div>
											</td>
											<td class="discount first-row"><h5>{{item.discount}}%</h5></td>
											<td class="total-price first-row"><h5>{{ formatCurrency(item.totalPrice) }}</h5></td>
											<td class="close-td first-row"><a @click="deleteItem(item._id)"><i class="ti-close fa-sharp fa-solid fa-circle-xmark"></i></a></td>
										</tr>
									</template >
									<template v-else>
										<tr>
											<td colspan="12"><h5 class="text-start p-4">Không có sản phẩm nào !!!</h5></td>
										</tr>
									</template>
								</tbody>
							</table>
						</div>
						<div class="row">
							<div class="col-lg-4"></div>
							<div class="col-lg-4 offset-lg-4">
								<div class="proceed-checkout">
									<a @click="clearCart" class="proceed-btn mb-3">Xóa tất cả</a>
									<ul>
										<li class="subtotal">Tổng số lượng <span v-if="listCart">{{totalQuantity}}</span></li>
										<li class="cart-total">Tổng tiền <span v-if="listCart">{{ formatCurrency(totalMoney) }}</span></li>
									</ul>
									<a @click="click" class="proceed-btn">Mua ngay</a>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>
  </div>
</template>

<script>
import { formatCurrency, showWarnToast } from "../../../assets/web/js/main";
import cartApi from "../../../service/Cart";
export default {
    data() {
        return {
			listCart: [],
			totalQuantity: 0,
			totalMoney: 0
        };
    },
    methods: {
		click(e){
			e.preventDefault()
			if(!sessionStorage.getItem("login")){
				window.location.href = '/auth/sign-in'
				sessionStorage.setItem("err", true)
			}
			if(this.listCart != "") this.$router.push("/order")
			else{
				this.$router.push("/store")
				sessionStorage.setItem("cart-empty",1)
			}
		},
		formatCurrency,
		async decreaseQty(item) {
			try{
				if (item.amount > 0) {  //Call API 
					item.amount--; 
					this.totalMoney -= item.totalPrice	// trừ hẳn tổng tiền cũ của sản phẩm
					item.totalPrice = item.price*item.amount - (item.price * item.amount * item.discount/100);

					this.totalQuantity= this.totalQuantity-1
					this.totalMoney += item.totalPrice	// cộng tổng tiền mới của sản phẩm

					await cartApi.editItemCart(item._id,-1)
					console.log("giam thanh cong")
				}
			}catch(err){
				console.log("loi giam ")
				console.log("err: "+err)
			}
			
		},
		async increaseQty(item) {
			try{
				if(item.quantity_in_stock >= item.amount)
				{
					item.amount++;
					this.totalMoney -= item.totalPrice
					item.totalPrice = item.price*item.amount - (item.price * item.amount * item.discount/100);
		
					this.totalQuantity = this.totalQuantity+1
					this.totalMoney += item.totalPrice
		
					await cartApi.editItemCart(item._id, 1)
						console.log("Tăng số lượng sản phẩm thành công");
				}
			}catch(err){
				showWarnToast("Sản phẩm đã hết hàng, vui lòng chọn sản phẩm khác !!");
				console.log("Lỗi: sản phẩm đã hết hàng");
				console.log("err: "+err)
			}
			
		},
		deleteItem(id) {
			cartApi.deleteItemCart(id)
				.then((res) => {
					console.log("xoa thanh cong")
					this.getItemIncart()
				})
				.catch(err => console.log("xoa khong thanh cong! : "+err))
		},
		async clearCart() {
			try{
				await cartApi.clearCart()
				await this.getItemIncart()
			}catch(err){
				console.log("clear that bai")
			}
		},
		async getItemIncart(){
			try{
				this.totalMoney = 0
				this.totalQuantity = 0
				const res = await cartApi.GetItemInCart()
				this.listCart = res.data
				for(var item of res.data){
					this.totalQuantity += item.amount
					this.totalMoney += item.totalPrice
				}
			}catch(err){
				console.log("loi trang cart !!! err: "+ err)
			}
		}
  	},
	mounted(){
		this.getItemIncart();
	},
}
</script>

<style>
.cart-title_name:hover{
	text-decoration: underline;
}

</style>