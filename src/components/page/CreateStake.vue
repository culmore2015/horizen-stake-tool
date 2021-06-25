<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-calendar"></i> 创建验证信息
                </el-breadcrumb-item>
                <el-breadcrumb-item>创建验证信息</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <div class="form-box">
                <el-form ref="form" :model="form" label-width="80px">
                    <el-form-item label="API KEY">
                        <el-input v-model="form.apikey" disabled="disabled"></el-input>
                    </el-form-item>

                    <el-form-item label="Stake地址">
                        <el-input v-model="form.stake_addr"></el-input>
                    </el-form-item>

                    <el-form-item label="奖励地址1">
                        <el-input v-model="form.rewards_addr_1"></el-input>
                    </el-form-item>
                    <el-form-item label="奖励分成1">
                        <el-input type="number" v-model="form.rewards_addr_1_pct"></el-input>
                    </el-form-item>
                    <el-form-item label="奖励地址2">
                        <el-input v-model="form.rewards_addr_2"></el-input>
                    </el-form-item>
                    <el-form-item label="奖励分成2">
                        <el-input type="number" v-model="form.rewards_addr_2_pct"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit">确认绑定</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
    import {Config} from '../../config/config';
    import {fetchZenSuperNodesCreateStake} from '../../api/index';
    import layer from "layui-layer";

    export default {
        name: 'baseform',
        data() {
            return {
                form: {
                    apikey: Config.apikey,
                    stake_addr: '',
                    rewards_addr_1: '',
                    rewards_addr_1_pct: 75,
                    rewards_addr_2: 'znRtPVpMpvCePCnivHf1Sdf3os41LXfbJfc',
                    rewards_addr_2_pct: 25,
                }
            };
        },
        methods: {
            onSubmit() {
                if (this.form.stake_addr === '') {
                    this.$message.error('Stake地址不能为空！');
                    return
                }
                if (this.form.rewards_addr_1 === '') {
                    this.$message.error('收益地址1不能为空！');
                    return
                }
                if ((parseInt(this.form.rewards_addr_1_pct) + parseInt(this.form.rewards_addr_2_pct)) !== 100) {
                    this.$message.error('分成比例总和必须为100！');
                    return
                }

                var index = layer.load(2)
                fetchZenSuperNodesCreateStake(this.form.stake_addr, this.form.rewards_addr_1, this.form.rewards_addr_1_pct, this.form.rewards_addr_2, this.form.rewards_addr_2_pct)
                    .then(res => {
                        console.log(res);
                        layer.alert(res.message);
                    }).catch(() => {
                    layer.alert('网络错误，请重试!');
                }).finally(() => {
                    layer.close(index)
                });
                //this.$message.success('提交成功！');
            }
        }
    };
</script>