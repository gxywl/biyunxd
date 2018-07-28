# _*_ encoding: utf-8 _*_
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, HiddenField, FileField, FloatField
from wtforms.validators import DataRequired, InputRequired
from ..models import Chanpin, Xiaoqu, Chanpinxx


# 客户
class KehuForm(FlaskForm):
    xiaoqu = SelectField('小区', validators=[DataRequired()], coerce=int)
    # donghao = StringField('栋号', validators=[DataRequired()])
    # fanghao = StringField('房号', validators=[DataRequired()])
    fangjian = StringField('栋单元房号', validators=[DataRequired()])
    chenghu = StringField('称呼', validators=[DataRequired()])
    tel = StringField('手机', validators=[DataRequired()])
    zje = FloatField('总金额')
    # status = SelectField('进度状态', validators=[DataRequired()],
    #                      choices=[('0', '已测尺'), ('1', '已下单'), ('2', '已安装'), ('3', '已清款')])
    status = SelectField('进度状态', validators=[DataRequired()], coerce=int)
    # 状态：测尺，已下单，已安装，已清款

    beizhu = StringField('备注')

    submit = SubmitField('确认保存')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(KehuForm, self).__init__(*args, **kwargs)
        self.xiaoqu.choices = [(xiaoqu.id, xiaoqu.xiaoqu) for xiaoqu in Xiaoqu.query.order_by(Xiaoqu.id).all()]
        self.status.choices = [(1, '已测尺'), (2, '已下单'), (3, '已安装'), (4, '已清款')]
    #     self.color.choices = [('0', '深灰'), ('1', '墨绿'), ('2', '白色')]


class WilladdcpForm(FlaskForm):
    chanpin = SelectField('选择产品', validators=[DataRequired()], coerce=int)

    submit = SubmitField('添加这个')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(WilladdcpForm, self).__init__(*args, **kwargs)
        self.chanpin.choices = [(chanpin.id, chanpin.pinming) for chanpin in
                                Chanpin.query.order_by(Chanpin.beizhu).all()]  # Chanpin.id
    #     self.color.choices = [('0', '深灰'), ('1', '墨绿'), ('2', '白色')]


# 入库员的过滤
class FineddidForm(FlaskForm):
    ddid = StringField('订单ID')
    status = SelectField('进度状态', coerce=int) #
    submit = SubmitField('开始过滤')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(FineddidForm, self).__init__(*args, **kwargs)
        self.status.choices = [(0, ''), (3, '已订货'), (4, '已入库')]
    #    self.chanpin.choices = [(chanpin.id, chanpin.pinming) for chanpin in Chanpin.query.order_by(Chanpin.beizhu).all()] # Chanpin.id
    #     self.color.choices = [('0', '深灰'), ('1', '墨绿'), ('2', '白色')]

# # 收货员的过滤
# class FineshddidForm(FlaskForm):
#     ddid = StringField('订单ID')
#     status = SelectField('进度状态', coerce=int) #
#     submit = SubmitField('开始过滤')
#
#     # 在构造化Form实例时指定selectField的choices内容,
#     def __init__(self, *args, **kwargs):
#         super(FineshddidForm, self).__init__(*args, **kwargs)
#         self.status.choices = [(0, ''), (3, '待收货'), (6, '已收货')]
#     #    self.chanpin.choices = [(chanpin.id, chanpin.pinming) for chanpin in Chanpin.query.order_by(Chanpin.beizhu).all()] # Chanpin.id
#     #     self.color.choices = [('0', '深灰'), ('1', '墨绿'), ('2', '白色')]

# 收货员的过滤
class FineshddidForm(FlaskForm):
    xiaoqu = SelectField('小区', coerce=int)
    fangjian = StringField('客户的房号 格式（x-x-xxxx）')
    chenghu = StringField('称呼')
    chanpin = SelectField('品类', coerce=int)
    status = SelectField('产品进度', coerce=int)
    submit = SubmitField('开始过滤')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(FineshddidForm, self).__init__(*args, **kwargs)
        self.chanpin.choices = [(0, '')] + [(chanpin.id, chanpin.pinming) for chanpin in
                                           Chanpin.query.order_by(Chanpin.beizhu).all()]
        self.xiaoqu.choices = [(0, '')] + [(xiaoqu.id, xiaoqu.xiaoqu) for xiaoqu in
                                           Xiaoqu.query.order_by(Xiaoqu.id).all()]
        self.status.choices = [(0, ''), (3, '待收货'), (6, '已收货')]
        # self.status.choices = [(0, ''), (1, '已量尺'), (2, '已下单'), (3, '已订货'), (4, '已入库'), (5, '已发货'), (6, '已收货'),
        #                        (7, '安装中'), (8, '安装完成'), (9, '已清款')]



# 发货员的过滤
class FinefhddidForm(FlaskForm):
    ddid = StringField('订单ID')
    status = SelectField('进度状态', coerce=int) #
    submit = SubmitField('开始过滤')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(FinefhddidForm, self).__init__(*args, **kwargs)
        self.status.choices = [(0, ''), (4, '已入库'), (5, '已发货')]
    #    self.chanpin.choices = [(chanpin.id, chanpin.pinming) for chanpin in Chanpin.query.order_by(Chanpin.beizhu).all()] # Chanpin.id
    #     self.color.choices = [('0', '深灰'), ('1', '墨绿'), ('2', '白色')]

# 派工员的过滤
class FinepgddidForm(FlaskForm):
    # ddid = StringField('订单ID')
    xiaoqu = SelectField('小区', coerce=int)
    fangjian = StringField('客户的房号 格式（x-x-xxxx）')
    # chenghu = StringField('称呼')
    status = SelectField('进度状态', coerce=int) #
    submit = SubmitField('开始过滤')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(FinepgddidForm, self).__init__(*args, **kwargs)
        self.xiaoqu.choices = [(0, '')] + [(xiaoqu.id, xiaoqu.xiaoqu) for xiaoqu in
                                           Xiaoqu.query.order_by(Xiaoqu.id).all()]
        self.status.choices = [(0, ''), (6, '未派工'), (7, '已派工'), (8, '已装完')]
    #    self.chanpin.choices = [(chanpin.id, chanpin.pinming) for chanpin in Chanpin.query.order_by(Chanpin.beizhu).all()] # Chanpin.id
    #     self.color.choices = [('0', '深灰'), ('1', '墨绿'), ('2', '白色')]

# 清款的过滤
class FineqkddidForm(FlaskForm):
    ddid = StringField('订单ID')
    status = SelectField('进度状态', coerce=int) #
    submit = SubmitField('开始过滤')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(FineqkddidForm, self).__init__(*args, **kwargs)
        self.status.choices = [(0, ''), (8, '已完成'), (9, '已清款')]
    #    self.chanpin.choices = [(chanpin.id, chanpin.pinming) for chanpin in Chanpin.query.order_by(Chanpin.beizhu).all()] # Chanpin.id
    #     self.color.choices = [('0', '深灰'), ('1', '墨绿'), ('2', '白色')]

# 业务员的过滤
class FindkhForm(FlaskForm):
    infostring = StringField('客户查找 「房号」或「称呼」或「电话」. 部分文字)')
    status = SelectField('产品进度', coerce=int)

    submit = SubmitField('开始过滤')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(FindkhForm, self).__init__(*args, **kwargs)
        self.status.choices = [(0, ''), (1, '已量尺'), (2, '已下单'), (3, '已订货'), (6, '已收货'),
                               (7, '安装中'), (8, '安装完成'), (9, '已清款')]  #, (4, '已入库'), (5, '已发货')
    #    self.chanpin.choices = [(chanpin.id, chanpin.pinming) for chanpin in Chanpin.query.order_by(Chanpin.beizhu).all()] # Chanpin.id
    #     self.color.choices = [('0', '深灰'), ('1', '墨绿'), ('2', '白色')]


# 客服的过滤
class KFfindForm(FlaskForm):
    xiaoqu = SelectField('小区', coerce=int)
    fangjian = StringField('客户的房号 格式（x-x-xxxx）')
    tel = StringField('电话.')
    status = SelectField('产品进度', coerce=int)
    submit = SubmitField('开始过滤')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(KFfindForm, self).__init__(*args, **kwargs)
        self.xiaoqu.choices = [(0, '')] + [(xiaoqu.id, xiaoqu.xiaoqu) for xiaoqu in
                                           Xiaoqu.query.order_by(Xiaoqu.id).all()]
        self.status.choices = [(0, ''), (1, '已量尺'), (2, '已下单'), (3, '已订货'), (6, '已收货'),
                               (7, '安装中'), (8, '安装完成'), (9, '已清款')] # (4, '已入库'), (5, '已发货'),


# 隐形网
class YxwForm(FlaskForm):
    # xiangmu = StringField("布放项目", validators=[DataRequired()])
    # xiangmu = SelectField('布放项目', validators=[DataRequired()], choices=[('0', '放生'),('1', '火施'),('2', '其他')])
    # cpid = HiddenField()
    # khid = HiddenField()
    # weizhi = SelectField('位置', validators=[DataRequired()], choices=[('', ''), ('大阳台', '大阳台'), ('小阳台', '小阳台')])
    weizhi = SelectField('位置', validators=[DataRequired()])
    shuliang = SelectField('数量', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    # xinghao = SelectField("型号", validators=[DataRequired()],
    #                       choices=[('', ''), ('恒大标配', '恒大标配'), ('标准型', '标准型'), ('普及型', '普及型')])
    xinghao = SelectField("型号", validators=[DataRequired()])
    kuan = IntegerField("宽（毫米）", validators=[DataRequired()])
    gao = IntegerField("高（毫米）", validators=[DataRequired()])
    color = SelectField("颜色", validators=[DataRequired()])
    beizhu = StringField('备注')
    uploadfile = FileField('上传图片/草图')

    # other = StringField("其他", validators=[DataRequired()])

    # jine = IntegerField("金额", validators=[DataRequired()])
    submit = SubmitField('保存修改')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(YxwForm, self).__init__(*args, **kwargs)
        self.weizhi.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'隐形网', chanshux=u'位置').order_by(Chanpinxx.chanshuz).all()]  # and Chanpinxx.chanshux == '位置'
        self.xinghao.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'隐形网', chanshux=u'型号').order_by(Chanpinxx.chanshuz).all()]
        self.color.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'隐形网', chanshux=u'颜色').order_by(Chanpinxx.chanshuz).all()]
        # self.color.choices = [('', ''), ('银色', '银色'), ('香槟色', '香槟色'), ('白色', '白色')]


# 纱门
class SmForm(FlaskForm):
    # weizhi = SelectField('位置', validators=[DataRequired()], choices=[('', ''), ('大阳台', '大阳台'), ('小阳台', '小阳台')])
    weizhi = SelectField('位置', validators=[DataRequired()])
    shuliang = SelectField('数量', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    # xinghao = SelectField("型号", validators=[DataRequired()],
    #                       choices=[('', ''), ('普及型', '普及型'), ('基本型', '基本型'), ('碧云801', '碧云801'), ('碧云804E', '碧云804E'),
    #                                ('碧云805E', '碧云805E')])
    xinghao = SelectField("型号", validators=[DataRequired()])
    kuan = IntegerField("宽（毫米）", validators=[DataRequired()])
    gao = IntegerField("高（毫米）", validators=[DataRequired()])
    neikuan = IntegerField("内空宽（毫米）", validators=[DataRequired()])
    color = SelectField("颜色", validators=[DataRequired()])
    shanshu = SelectField('扇数', validators=[DataRequired()], choices=[('', ''), ('1', '1'), ('2', '2')])
    zhonghengtiaoshu = SelectField('中横条数', validators=[DataRequired()], choices=[('', ''), ('1', '1'), ('2', '2')])
    shuowei = SelectField('锁位', validators=[DataRequired()],
                          choices=[('', ''), ('中', '中'), ('左', '左'), ('右', '右'), ('上', '上'), ('下', '下')])
    zhangfa = SelectField('装法', validators=[DataRequired()],
                          choices=[('', ''), ('内装', '内装'), ('外装', '外装')])
    beizhu = StringField('备注')
    uploadfile = FileField('上传图片/草图')

    # other = StringField("其他", validators=[DataRequired()])

    # jine = IntegerField("金额", validators=[DataRequired()])
    submit = SubmitField('保存修改')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(SmForm, self).__init__(*args, **kwargs)
        self.weizhi.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'纱门', chanshux=u'位置').order_by(Chanpinxx.chanshuz).all()]  # and Chanpinxx.chanshux == '位置'
        self.xinghao.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'纱门', chanshux=u'型号').order_by(Chanpinxx.chanshuz).all()]
        self.color.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'纱门', chanshux=u'颜色').order_by(Chanpinxx.chanshuz).all()]
        # self.color.choices = [('深灰', '深灰')]


# 晾衣杆
class LygForm(FlaskForm):
    # weizhi = SelectField('位置', validators=[DataRequired()], choices=[('', ''), ('大阳台', '大阳台'), ('小阳台', '小阳台')])
    weizhi = SelectField('位置', validators=[DataRequired()])
    shuliang = SelectField('数量', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    # xinghao = SelectField("型号", validators=[DataRequired()],
    #                       choices=[('', ''), ('G1-25', 'G1-25'), ('G2-32', 'G2-32'), ('G3-32', 'G3-32'), ('手摇型', '手摇型')])
    xinghao = SelectField("型号", validators=[DataRequired()])
    chang = IntegerField("长（毫米）", validators=[DataRequired()])
    gao = IntegerField("高（毫米）", validators=[DataRequired()])


    gantiaoshu = SelectField('杆条数', validators=[DataRequired()], choices=[('', ''), ('1', '1'), (2, '2')])
    color = SelectField("颜色", validators=[DataRequired()])

    beizhu = StringField('备注')
    uploadfile = FileField('上传图片/草图')

    # other = StringField("其他", validators=[DataRequired()])

    # jine = IntegerField("金额", validators=[DataRequired()])
    submit = SubmitField('保存修改')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(LygForm, self).__init__(*args, **kwargs)
        self.weizhi.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'晾衣杆', chanshux=u'位置').order_by(Chanpinxx.chanshuz).all()]  # and Chanpinxx.chanshux == '位置'
        self.xinghao.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'晾衣杆', chanshux=u'型号').order_by(Chanpinxx.chanshuz).all()]
        self.color.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'晾衣杆', chanshux=u'颜色').order_by(Chanpinxx.chanshuz).all()]
        # self.color.choices = [('', ''), ('白', '白'), ('银色', '银色'), ('香槟金', '香槟金')]


# 晾衣机
class LyjForm(FlaskForm):
    # weizhi = SelectField('位置', validators=[DataRequired()], choices=[('', ''), ('大阳台', '大阳台'), ('小阳台', '小阳台')])
    weizhi = SelectField('位置', validators=[DataRequired()])
    shuliang = SelectField('数量', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    # xinghao = SelectField("型号", validators=[DataRequired()], choices=[('', ''), ('BY-02', 'BY-02'), (' BY-06', ' BY-06')])
    xinghao = SelectField("型号", validators=[DataRequired()])
    chang = IntegerField("长（毫米）", validators=[DataRequired()])
    gao = IntegerField("高（毫米）", validators=[DataRequired()])
    gantiaoshu = SelectField('杆条数', validators=[DataRequired()], choices=[('4', '4'), ('2', '2'), ('3', '3')])
    color = SelectField("颜色", validators=[DataRequired()])

    beizhu = StringField('备注')
    uploadfile = FileField('上传图片/草图')

    # other = StringField("其他", validators=[DataRequired()])

    # jine = IntegerField("金额", validators=[DataRequired()])
    submit = SubmitField('保存修改')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(LyjForm, self).__init__(*args, **kwargs)
        self.weizhi.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'晾衣机', chanshux=u'位置').order_by(Chanpinxx.chanshuz).all()]  # and Chanpinxx.chanshux == '位置'
        self.xinghao.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'晾衣机', chanshux=u'型号').order_by(Chanpinxx.chanshuz).all()]
        self.color.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'晾衣机', chanshux=u'颜色').order_by(Chanpinxx.chanshuz).all()]
        # self.color.choices = [('', ''), ('香槟金', '香槟金'), ('太空银', '太空银')]


# 纱窗
class ScForm(FlaskForm):
    # weizhi = SelectField('位置', validators=[DataRequired()],
    #                      choices=[('', ''), ('主卧', '主卧'), ('次卧', '次卧'), ('客房', '客房'), ('书房', '书房'), ('衣帽间', '衣帽间'),
    #                               ('厨房', '厨房'), ('主卫', '主卫'), ('公卫', '公卫'), ('其他', '其他')])
    weizhi = SelectField('位置', validators=[DataRequired()])
    shuliang = SelectField('数量', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    # xinghao = SelectField("型号", validators=[DataRequired()],
    #                       choices=[('', ''), ('ST613', 'ST613'), ('不可拆左右趟', '不可拆左右趟'), ('可拆左右趟', '可拆左右趟'), ('普及上下趟', '普及上下趟')])
    xinghao = SelectField("型号", validators=[DataRequired()])
    kuan = IntegerField("宽（毫米）", validators=[DataRequired()])
    gao = IntegerField("高（毫米）", validators=[DataRequired()])
    # digao= IntegerField("底高（毫米）", validators=[DataRequired()])
    bashoudg = IntegerField("把手底高（毫米）", validators=[DataRequired()])
    shuowei = SelectField('锁位', validators=[DataRequired()],
                          choices=[('', ''), ('左', '左'), ('右', '右'),('左右锁', '左右锁'),('底锁', '底锁')])  # , ('下', '下')
    color = SelectField("颜色", validators=[DataRequired()])

    dengfenshu = SelectField('等分数', validators=[DataRequired()],
                             choices=[('', ''), ('无', '无'), ('2等分', '2等分'), ('平均3等分', '平均3等分'), ('非平均3等分', '非平均3等分')])
    ishaveht = SelectField('横条数', validators=[DataRequired()], choices=[('0', '无横条'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])

    beizhu = StringField('备注')
    uploadfile = FileField('上传图片/草图')

    # other = StringField("其他", validators=[DataRequired()])

    # jine = IntegerField("金额", validators=[DataRequired()])
    submit = SubmitField('保存修改')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(ScForm, self).__init__(*args, **kwargs)
        self.weizhi.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'纱窗', chanshux=u'位置').order_by(Chanpinxx.chanshuz).all()]  # and Chanpinxx.chanshux == '位置'
        self.xinghao.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'纱窗', chanshux=u'型号').order_by(Chanpinxx.chanshuz).all()]
        self.color.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'纱窗', chanshux=u'颜色').order_by(Chanpinxx.chanshuz).all()]
        # self.color.choices = [('深灰', '深灰')]


# 窗花
class ChForm(FlaskForm):
    # weizhi = SelectField('位置', validators=[DataRequired()],
    #                      choices=[('', ''), ('主卧', '主卧'), ('次卧', '次卧'), ('客房', '客房'), ('书房', '书房'), ('衣帽间', '衣帽间'),
    #                               ('厨房', '厨房'), ('主卫', '主卫'), ('公卫', '公卫'), ('其他', '其他')])
    weizhi = SelectField('位置', validators=[DataRequired()])
    shuliang = SelectField('数量', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    # xinghao = SelectField("型号", validators=[DataRequired()],
    #                       choices=[('', ''), ('一帆风顺-带纱', '一帆风顺-带纱'), ('双喜临门-带纱', '双喜临门-带纱'), ('心心相印-带纱', '心心相印-带纱'), ('招财进宝-带纱', '招财进宝-带纱')])
    xinghao = SelectField("型号", validators=[DataRequired()])
    kuan = IntegerField("宽（毫米）", validators=[DataRequired()])
    gao = IntegerField("高（毫米）", validators=[DataRequired()])
    # digao= IntegerField("底高（毫米）", validators=[DataRequired()])
    bashoudg = IntegerField("把手底高（毫米）", validators=[DataRequired()])
    shuowei = SelectField('锁位', validators=[DataRequired()],
                          choices=[('', ''), ('左', '左'), ('右', '右'), ('上', '上'), ('下', '下'),('左右锁', '左右锁')])  # ( '中', '中'),
    color = SelectField("颜色", validators=[DataRequired()])

    # dengfenshu = SelectField('等分数', validators=[DataRequired()],
    #                          choices=[('', ''), ('无', '无'), ('2等分', '2等分'), ('平均3等分', '平均3等分'), ('非平均3等分', '非平均3等分')])
    # ishaveht = SelectField('有否横条', validators=[DataRequired()], choices=[('', ''), ('无横条', '无横条'), ('有横条', '有横条')])

    beizhu = StringField('备注')
    uploadfile = FileField('上传图片/草图')

    # other = StringField("其他", validators=[DataRequired()])

    # jine = IntegerField("金额", validators=[DataRequired()])
    submit = SubmitField('保存修改')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(ChForm, self).__init__(*args, **kwargs)
        self.weizhi.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'窗花', chanshux=u'位置').order_by(Chanpinxx.chanshuz).all()]  # and Chanpinxx.chanshux == '位置'
        self.xinghao.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'窗花', chanshux=u'型号').order_by(Chanpinxx.chanshuz).all()]
        self.color.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'窗花', chanshux=u'颜色').order_by(Chanpinxx.chanshuz).all()]
        # self.color.choices = [('深灰', '深灰')]


# 指纹锁
class ZwsForm(FlaskForm):
    # weizhi = SelectField('位置', validators=[DataRequired()], choices=[('', ''), ('客厅', '客厅')])
    weizhi = SelectField('位置', validators=[DataRequired()])
    shuliang = SelectField('数量', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    # xinghao = SelectField("型号", validators=[DataRequired()],
    #                       choices=[('', ''), ('9001', '9001'), ('935', '935'), ('938', '938'), ('普及型', '普及型')])
    xinghao = SelectField("型号", validators=[DataRequired()])
    color = SelectField("颜色", validators=[DataRequired()])
    shuowei = SelectField('锁位', validators=[DataRequired()],
                          choices=[('', ''), ('左', '左'), ('右', '右')])
    kaishuofs = SelectField('开锁方式', validators=[DataRequired()],
                            choices=[('', ''), ('内开', '内开'), ('外开', '外开')])
    # bashoudg = IntegerField("把手底高（毫米）", validators=[DataRequired()])

    beizhu = StringField('备注')
    uploadfile = FileField('上传图片/草图')

    # other = StringField("其他", validators=[DataRequired()])

    # jine = IntegerField("金额", validators=[DataRequired()])
    submit = SubmitField('保存修改')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(ZwsForm, self).__init__(*args, **kwargs)
        self.weizhi.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'指纹锁', chanshux=u'位置').order_by(Chanpinxx.chanshuz).all()]  # and Chanpinxx.chanshux == '位置'
        self.xinghao.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'指纹锁', chanshux=u'型号').order_by(Chanpinxx.chanshuz).all()]
        self.color.choices = [(chanpinxx.chanshuz, chanpinxx.chanshuz) for chanpinxx in Chanpinxx.query.filter_by(
            pinming=u'指纹锁', chanshux=u'颜色').order_by(Chanpinxx.chanshuz).all()]
        # self.color.choices = [('', ''), ('古铜红', '古铜红'), ('香槟金', '香槟金')]


class NameForm(FlaskForm):
    # xiangmu = StringField("布放项目", validators=[DataRequired()])
    # xiangmu = SelectField('布放项目', validators=[DataRequired()], choices=[('0', '放生'),('1', '火施'),('2', '其他')])
    # xiangmu = SelectField('产品', validators=[DataRequired()], coerce=int)
    # weizhi = SelectField('位置', validators=[DataRequired()], choices=[('0', '阳台'), ('1', '客厅'), ('2', '餐厅')])
    # color = SelectField("颜色", validators=[DataRequired()])
    # suoweizhi = SelectField('锁位', validators=[DataRequired()],
    #                         choices=[('0', '中'), ('1', '左'), ('2', '右'), ('3', '上'), ('4', '下')])
    #
    # # othercolor = StringField("另定颜色", validators=[DataRequired()])
    # zhongchang = IntegerField("总长", validators=[DataRequired()])
    # lidigao = IntegerField("离底", validators=[DataRequired()])
    # chang = IntegerField("长", validators=[DataRequired()])
    # kuan = IntegerField("宽", validators=[DataRequired()])
    # gao = IntegerField("高", validators=[DataRequired()])
    #
    # other = StringField("其他", validators=[DataRequired()])
    #
    # # jine = IntegerField("金额", validators=[DataRequired()])
    # submit = SubmitField('确认下单')
    #
    # # 在构造化Form实例时指定selectField的choices内容,
    # def __init__(self, *args, **kwargs):
    #     super(NameForm, self).__init__(*args, **kwargs)
    #     self.xiangmu.choices = [(xiangmu.id, xiangmu.xiangmu) for xiangmu in Xiangmu.query.order_by(Xiangmu.id).all()]
    #     self.color.choices = [('', ''), ('深灰', '深灰'), ('墨绿', '墨绿'), ('白色', '白色')]
    pass

# class EditProfileForm(FlaskForm):
