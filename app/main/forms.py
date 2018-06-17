# _*_ encoding: utf-8 _*_
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, HiddenField, FileField
from wtforms.validators import DataRequired, InputRequired
from ..models import Chanpin, Xiaoqu


class KehuForm(FlaskForm):

    xiaoqu = SelectField('小区', validators=[DataRequired()], coerce=int)
    donghao = StringField('栋号', validators=[DataRequired()])
    fanghao = StringField('房号', validators=[DataRequired()])
    chenghu = StringField('称呼', validators=[DataRequired()])
    tel = StringField('手机', validators=[DataRequired()])

    submit = SubmitField('确认保存')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(KehuForm, self).__init__(*args, **kwargs)
        self.xiaoqu.choices = [(xiaoqu.id, xiaoqu.xiaoqu) for xiaoqu in Xiaoqu.query.order_by(Xiaoqu.id).all()]
    #     self.color.choices = [('0', '深灰'), ('1', '墨绿'), ('2', '白色')]

class WilladdcpForm(FlaskForm):

    chanpin = SelectField('选择产品', validators=[DataRequired()], coerce=int)

    submit = SubmitField('添加这个')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(WilladdcpForm, self).__init__(*args, **kwargs)
        self.chanpin.choices = [(chanpin.id, chanpin.pinming) for chanpin in Chanpin.query.order_by(Chanpin.id).all()]
    #     self.color.choices = [('0', '深灰'), ('1', '墨绿'), ('2', '白色')]

class YxwForm(FlaskForm):
    # xiangmu = StringField("布放项目", validators=[DataRequired()])
    # xiangmu = SelectField('布放项目', validators=[DataRequired()], choices=[('0', '放生'),('1', '火施'),('2', '其他')])
    # cpid = HiddenField()
    # khid = HiddenField()
    weizhi = SelectField('位置', validators=[DataRequired()], choices=[('阳台', '阳台'), ('客厅', '客厅'), ('餐厅', '餐厅')])
    shuliang = SelectField('数量', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    xinghao = StringField("型号", validators=[DataRequired()])
    kuan = IntegerField("宽（毫米）", validators=[DataRequired()])
    gao = IntegerField("高（毫米）", validators=[DataRequired()])
    color = SelectField("颜色", validators=[DataRequired()])

    uploadfile = FileField('选择文件')

    # other = StringField("其他", validators=[DataRequired()])

    # jine = IntegerField("金额", validators=[DataRequired()])
    submit = SubmitField('确认订制')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(YxwForm, self).__init__(*args, **kwargs)
        #self.xiangmu.choices = [(xiangmu.id, xiangmu.xiangmu) for xiangmu in Xiangmu.query.order_by(Xiangmu.id).all()]
        self.color.choices = [('深灰', '深灰'), ('墨绿', '墨绿'), ('白色', '白色')]

class SmForm(FlaskForm):
    weizhi = SelectField('位置', validators=[DataRequired()], choices=[('阳台', '阳台'), ('客厅', '客厅'), ('餐厅', '餐厅')])
    shuliang = SelectField('数量', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    xinghao = StringField("型号", validators=[DataRequired()])
    kuan = IntegerField("宽（毫米）", validators=[DataRequired()])
    gao = IntegerField("高（毫米）", validators=[DataRequired()])
    color = SelectField("颜色", validators=[DataRequired()])
    neikuan = IntegerField("内空宽（毫米）", validators=[DataRequired()])
    shanshu = SelectField('扇数', validators=[DataRequired()], choices=[('1', '1'), ('2', '2')])
    zhonghengtiaoshu = SelectField('中横条数', validators=[DataRequired()], choices=[('1', '1'), ('2', '2')])
    shuowei = SelectField('锁位', validators=[DataRequired()],
                            choices=[('中', '中'), ('左', '左'), ('右', '右'), ('上', '上'), ('下', '下')])
    zhangfa = SelectField('装法', validators=[DataRequired()],
                            choices=[('内装', '内装'), ('外装', '外装')])
    # other = StringField("其他", validators=[DataRequired()])

    # jine = IntegerField("金额", validators=[DataRequired()])
    submit = SubmitField('确认订制')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(SmForm, self).__init__(*args, **kwargs)
        #self.xiangmu.choices = [(xiangmu.id, xiangmu.xiangmu) for xiangmu in Xiangmu.query.order_by(Xiangmu.id).all()]
        self.color.choices = [('深灰', '深灰'), ('墨绿', '墨绿'), ('白色', '白色')]


class LyjForm(FlaskForm):

    weizhi = SelectField('位置', validators=[DataRequired()], choices=[('阳台', '阳台'), ('客厅', '客厅'), ('餐厅', '餐厅')])
    shuliang = SelectField('数量', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    xinghao = StringField("型号", validators=[DataRequired()])
    chang = IntegerField("长（毫米）", validators=[DataRequired()])
    gao = IntegerField("高（毫米）", validators=[DataRequired()])
    gantiaoshu = SelectField('杆条数', validators=[DataRequired()], choices=[('1', '1'), ('2', '2')])
    color = SelectField("颜色", validators=[DataRequired()])

    # other = StringField("其他", validators=[DataRequired()])

    # jine = IntegerField("金额", validators=[DataRequired()])
    submit = SubmitField('确认订制')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(LyjForm, self).__init__(*args, **kwargs)
        #self.xiangmu.choices = [(xiangmu.id, xiangmu.xiangmu) for xiangmu in Xiangmu.query.order_by(Xiangmu.id).all()]
        self.color.choices = [('深灰', '深灰'), ('墨绿', '墨绿'), ('白色', '白色')]


class ScForm(FlaskForm):
    weizhi = SelectField('位置', validators=[DataRequired()], choices=[('阳台', '阳台'), ('客厅', '客厅'), ('餐厅', '餐厅')])
    shuliang = SelectField('数量', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    xinghao = StringField("型号", validators=[DataRequired()])
    kuan = IntegerField("宽（毫米）", validators=[DataRequired()])
    gao = IntegerField("高（毫米）", validators=[DataRequired()])
    color = SelectField("颜色", validators=[DataRequired()])
    digao= IntegerField("底高（毫米）", validators=[DataRequired()])
    dengfenshu = SelectField('等分数', validators=[DataRequired()], choices=[('2等分', '2等分'), ('平均3等分', '平均3等分'), ('非平均3等分', '非平均3等分')])
    ishaveht = SelectField('有否横条', validators=[DataRequired()], choices=[('0', '无横条'), ('1', '有横条')])
    shuowei = SelectField('锁位', validators=[DataRequired()],
                            choices=[('中', '中'), ('左', '左'), ('右', '右'), ('上', '上'), ('下', '下')])

    # other = StringField("其他", validators=[DataRequired()])

    # jine = IntegerField("金额", validators=[DataRequired()])
    submit = SubmitField('确认订制')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(ScForm, self).__init__(*args, **kwargs)
        #self.xiangmu.choices = [(xiangmu.id, xiangmu.xiangmu) for xiangmu i
        self.color.choices = [('深灰', '深灰'), ('墨绿', '墨绿'), ('白色', '白色')]


class ZwsForm(FlaskForm):
    weizhi = SelectField('位置', validators=[DataRequired()], choices=[('阳台', '阳台'), ('客厅', '客厅'), ('餐厅', '餐厅')])
    shuliang = SelectField('数量', validators=[DataRequired()], choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    xinghao = StringField("型号", validators=[DataRequired()])
    color = SelectField("颜色", validators=[DataRequired()])
    shuowei = SelectField('锁位', validators=[DataRequired()],
                            choices=[('中', '中'), ('左', '左'), ('右', '右'), ('上', '上'), ('下', '下')])

    # other = StringField("其他", validators=[DataRequired()])

    # jine = IntegerField("金额", validators=[DataRequired()])
    submit = SubmitField('确认订制')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(ZwsForm, self).__init__(*args, **kwargs)
        #self.xiangmu.choices = [(xiangmu.id, xiangmu.xiangmu) for xiangmu i
        self.color.choices = [('深灰', '深灰'), ('墨绿', '墨绿'), ('白色', '白色')]

class NameForm(FlaskForm):
    # xiangmu = StringField("布放项目", validators=[DataRequired()])
    # xiangmu = SelectField('布放项目', validators=[DataRequired()], choices=[('0', '放生'),('1', '火施'),('2', '其他')])
    xiangmu = SelectField('产品', validators=[DataRequired()], coerce=int)
    weizhi = SelectField('位置', validators=[DataRequired()], choices=[('0', '阳台'), ('1', '客厅'), ('2', '餐厅')])
    color = SelectField("颜色", validators=[DataRequired()])
    suoweizhi = SelectField('锁位', validators=[DataRequired()],
                            choices=[('0', '中'), ('1', '左'), ('2', '右'), ('3', '上'), ('4', '下')])

    # othercolor = StringField("另定颜色", validators=[DataRequired()])
    zhongchang = IntegerField("总长", validators=[DataRequired()])
    lidigao = IntegerField("离底", validators=[DataRequired()])
    chang = IntegerField("长", validators=[DataRequired()])
    kuan = IntegerField("宽", validators=[DataRequired()])
    gao = IntegerField("高", validators=[DataRequired()])

    other = StringField("其他", validators=[DataRequired()])

    # jine = IntegerField("金额", validators=[DataRequired()])
    submit = SubmitField('确认下单')

    # 在构造化Form实例时指定selectField的choices内容,
    def __init__(self, *args, **kwargs):
        super(NameForm, self).__init__(*args, **kwargs)
        self.xiangmu.choices = [(xiangmu.id, xiangmu.xiangmu) for xiangmu in Xiangmu.query.order_by(Xiangmu.id).all()]
        self.color.choices = [('深灰', '深灰'), ('墨绿', '墨绿'), ('白色', '白色')]

# class EditProfileForm(FlaskForm):
