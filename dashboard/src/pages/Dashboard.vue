<template>
  <div class="content">
    <div class="md-layout">
      <div
        class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-30"
      >
        <stats-card data-background-color="green">
          <template slot="header">
            <md-icon>arrow_circle_up</md-icon>
          </template>

          <template slot="content">
            <p class="category">昨日新增发帖数</p>
            <h3 class="title">+ {{ newposts }}</h3>
          </template>

          <template slot="footer">
            <div class="stats">
              <md-icon>date_range</md-icon>
              Last 24 Hours
            </div>
          </template>
        </stats-card>
      </div>
      <div
        class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-30"
      >
        <stats-card data-background-color="orange">
          <template slot="header">
            <md-icon>trending_up</md-icon>
          </template>

          <template slot="content">
            <p class="category">昨日新增评论数</p>
            <h3 class="title">+ {{ newcomments }}</h3>
          </template>

          <template slot="footer">
            <div class="stats">
              <md-icon class="text-danger">date_range</md-icon>
              Last 24 Hours
            </div>
          </template>
        </stats-card>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <md-card>
          <md-card-header data-background-color="orange">
            <h4 class="title">标题关键词词云</h4>
            <p class="category">最近更新 24 小时</p>
          </md-card-header>
          <md-card-content>
            <div
              :style="{ width: '100%', height: '600px' }"
              id="threadWordCloud"
            ></div>
          </md-card-content>
        </md-card>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <md-card>
          <md-card-header data-background-color="orange">
            <h4 class="title">帖子词云图</h4>
            <p class="category">最近更新 24 小时</p>
          </md-card-header>
          <md-card-content>
            <div
              :style="{ width: '100%', height: '600px' }"
              id="postWordCloud"
            ></div>
          </md-card-content>
        </md-card>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <md-card>
          <md-card-header data-background-color="orange">
            <h4 class="title">评论词云图</h4>
            <p class="category">最近更新 24 小时</p>
          </md-card-header>
          <md-card-content>
            <div
              :style="{ width: '100%', height: '600px' }"
              id="commentWordCloud"
            ></div>
          </md-card-content>
        </md-card>
      </div>
    </div>
  </div>
</template>

<script>
import { StatsCard } from "@/components";
import "echarts-wordcloud/dist/echarts-wordcloud.min";

export default {
  components: {
    StatsCard,
  },
  data() {
    return {
      threadWordCloud: [],
      postWordCloud: [],
      commentWordCloud: [],
      newposts: 0,
      newcomments: 0,
    };
  },
  methods: {
    getThreadWorldCloud() {
      let chart = this.$echarts.init(
        document.getElementById("threadWordCloud")
      );
      let option = {
        backgroundColor: "#fff",
        series: [
          {
            type: "wordCloud",
            gridSize: 10,
            sizeRange: [14, 60],
            rotationRange: [0, 0],
            left: "center",
            top: "center",
            right: null,
            bottom: null,
            width: "200%",
            height: "200%",
            //数据
            data: [],
          },
        ],
      };
      chart.showLoading();
      this.$axios
        .get("http://123.249.35.243:5000/thread/wordcloud")
        .then((res) => {
          console.log(res.data.data);
          this.threadWordCloud = res.data.data;
          option.series[0].data = this.threadWordCloud;
          chart.setOption(option);
          chart.hideLoading();
        });
    },
    getPostWorldCloud() {
      let chart = this.$echarts.init(document.getElementById("postWordCloud"));
      let option = {
        backgroundColor: "#fff",
        series: [
          {
            type: "wordCloud",
            gridSize: 10,
            sizeRange: [14, 60],
            rotationRange: [0, 0],
            left: "center",
            top: "center",
            right: null,
            bottom: null,
            width: "200%",
            height: "200%",
            //数据
            data: [],
          },
        ],
      };
      chart.showLoading();
      this.$axios
        .get("http://123.249.35.243:5000/post/wordcloud")
        .then((res) => {
          console.log(res.data.data);
          this.postWordCloud = res.data.data;
          option.series[0].data = this.postWordCloud;
          chart.setOption(option);
          chart.hideLoading();
        });
    },
    getCommentWordCloud() {
      let chart = this.$echarts.init(
        document.getElementById("commentWordCloud")
      );
      let option = {
        backgroundColor: "#fff",
        series: [
          {
            type: "wordCloud",
            gridSize: 10,
            sizeRange: [14, 60],
            rotationRange: [0, 0],
            left: "center",
            top: "center",
            right: null,
            bottom: null,
            width: "200%",
            height: "200%",
            //数据
            data: [],
          },
        ],
      };
      chart.showLoading();
      this.$axios
        .get("http://123.249.35.243:5000/comment/wordcloud")
        .then((res) => {
          console.log(res.data.data);
          this.commentWordCloud = res.data.data;
          option.series[0].data = this.commentWordCloud;
          chart.setOption(option);
          chart.hideLoading();
        });
    },
    getNewPost() {
      this.$axios
        .get("http://123.249.35.243:5000/yesterday/post")
        .then((res) => {
          console.log(res.data.data);
          this.newposts = res.data.data;
        });
    },
    getNewComment() {
      this.$axios
        .get("http://123.249.35.243:5000/yesterday/comment")
        .then((res) => {
          console.log(res.data.data);
          this.newcomments = res.data.data;
        });
    },
  },
  mounted() {
    this.getThreadWorldCloud();
    this.getPostWorldCloud();
    this.getCommentWordCloud();
    this.getNewPost();
    this.getNewComment();
  },
};
</script>
