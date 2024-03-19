<template>
  <div>
    <head>
      <title>Admin Page</title>
    </head>
    <div id="toast"></div>
    <section class="content-header">
      <div class="container-fluid">
        <div class="row mb-2">
          <div class="col-sm-6">
            <h1>Trang chủ</h1>
          </div>
          <div class="row gy-4 mb-3">
            <!-- Congratulations card -->
            <div v-for="cardItem in cardItems" :key="cardItem.id" class="col-md-12 col-lg-3">
              <div class="card">
                <div class="card-body">
                  <div class="card-circle">
                    <i :class="`card-icon fa-solid ${cardItem.icon}`"></i>
                  </div>
                  <div class="card-content">
                    <h4 class="card-label">{{ cardItem.label }}</h4>
                    <p class="mb-2 pb-1">{{ cardItem.value }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- <div class="d-flex">
            <div class="filter-statistical">
              <select class="form-control form-select" v-model="this.selectedFilter" @change="updateSelect()">
                <option selected="selected" value="1">Thống kê theo tháng</option>
				<option value="2">Thống kê theo khoảng ngày</option>
              </select>
              <ul v-if="this.selectedFilter == 1">
                <label style="padding-top: 10px;">Thống kê doanh thu theo năm</label>
                <li v-for="year in years" :key="year" :value="year" @click="update(year)" style="cursor: pointer; width: 300px;">
                  Năm {{ year }}: {{ formatCurrency(revenueWithYear[year]) }}
                </li>
              </ul>
              <ul v-if="this.selectedFilter == 2">
                <div class="statistical">
                  <label class="statistical-from" for="startDate">Từ ngày:</label>
                  <VueDatePicker v-model="startDate" format="yyyy-MM-dd"></VueDatePicker>
                  <label class="statistical-from" for="endDate">Đến ngày:</label>
                  <VueDatePicker v-model="endDate" format="yyyy-MM-dd"></VueDatePicker>
                  <button class="statistical-btn btn btn-primary" @click="thongKe">Thống kê</button>
                </div>
              </ul>
            </div>
            <div style="width: 1000px; height: 600px;">
              <canvas id="myChart"></canvas>
            </div>
          </div>-->
        </div> 
      </div>
    </section>
  </div>
</template>

<script>
// import VueDatePicker from '@vuepic/vue-datepicker';
// import '@vuepic/vue-datepicker/dist/main.css'
// import Chart from 'chart.js/auto'
import revenueApi from '../../../service/revenue';
import { showErrorToastMess } from "../../../assets/web/js/main";
import { formatDate, formatCurrency } from "../../../assets/admin/js/format-admin";

export default {
	// components: {
	// 	VueDatePicker
	// },
	data() {
		return {
			selectedFilter: 1,
			years: [],
			revenue: [],
			revenueWithYear: {},
			myChart: null,
			startDate: null,
			endDate: null,
			cardItems: [
				{ id: 1, label: 'TỔNG ĐƠN', data_name: "orders" , value: null, icon: 'fa-calendar' },
				{ id: 2, label: 'TỔNG SẢN PHẨM', data_name: "products" , value: null, icon: 'fa-hand-holding-dollar' },
				{ id: 3, label: 'Người dùng đăng ký', data_name: "users" , value: null, icon: 'fa-user' },
				{ id: 4, label: 'Đơn hàng chờ xử lý', data_name: "orders_pending" , value: null, icon: 'fa-clipboard' }
			]
		}
	},
	methods: {
		formatDate,
		formatCurrency,
		async getCard() {
			try {
				const res = await revenueApi.getCard()
				this.cardItems.forEach(cardItem => {
				cardItem.value = res[cardItem.data_name];
				});
			} catch (err) {
				console.log("err: " + err)
			}
		},
	},
	mounted() {
		if (!sessionStorage.getItem("login") && sessionStorage.getItem("role") !== "admin") {
			this.$router.push("/auth/sign-in")
			sessionStorage.setItem("auth", true)
		}
		this.getCard()
	}
}
</script>

<style>
@import url(../../../assets/admin/css/home.css);
</style>
