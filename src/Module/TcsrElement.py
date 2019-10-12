from src.Module.CircuitBasic import *
from src.ConstantType import Constant


########################################################################################################################

# 发送器模型
class TcsrPower(ElePack):
    new_table = {
        '发送器内阻': 'z',
        '发送电平级': 'level',
    }
    prop_table = ElePack.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base)
        self.flag_ele_list = True
        self.add_child('1电压源', OPortPowerU(self, '1电压源', voltage=parent_ins.pwr_voltage))
        self.add_child('2内阻', TcsrPowerZ(self, '2内阻', z))


    @property
    def z(self):
        return self.element['2内阻'].z

    @z.setter
    def z(self, value):
        self.element['2内阻'].z = value

    @property
    def level(self):
        return self.parent_ins.send_level

    @level.setter
    def level(self, value):
        self.parent_ins.send_level = value


# 移频脉冲发送器
class TcsrPowerYPMC(TcsrPower):
    def __init__(self, parent_ins, name_base, z, z_iso):
        super().__init__(parent_ins, name_base, z)
        self.add_child('3隔离元件', TPortZSeries(self, '3隔离元件', z_iso))


########################################################################################################################

# 发送器内阻
class TcsrPowerZ(TPortZSeries):
    new_table = {
        '电平级': 'level'
    }
    prop_table = TPortZSeries.prop_table.copy()
    prop_table.update(new_table)

    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base, z)

    @property
    def level(self):
        return self.parent_ins.level

    @level.setter
    def level(self, value):
        self.parent_ins.level = value

    def get_coeffs(self, freq):
        z = self.z[self.level][freq].z
        self.value2coeffs(z)
        return self.equs


########################################################################################################################

# 接收器
class TcsrReceiver(OPortZ):
    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base, z)


# 移频脉冲接收器
class TcsrReceiverYPMC(ElePack):
    def __init__(self, parent_ins, name_base, z_iso2, z_iso, z_rcv):
        super().__init__(parent_ins, name_base)
        self.flag_ele_list = True
        self.add_child('0接收器', OPortZ(self, '0接收器', z_rcv))
        self.add_child('1隔离元件', TPortZSeries(self, '1隔离元件', z_iso))
        self.add_child('2隔离元件', TPortZParallel(self, '2隔离元件', z_iso2))


########################################################################################################################

# 变压器模板
class TcsrTransformer(ElePack):
    def __init__(self, parent_ins, name_base, z1, z2, n):
        super().__init__(parent_ins, name_base)
        self.flag_ele_list = True
        self.add_child('1等效内阻', TPortCircuitT(self, '1等效内阻', z1, z2, z1))
        self.add_child('2变压器', TPortCircuitN(self, '2变压器', n))


# 开短路模型变压器模板
class TcsrTransformerOpenShort(ElePack):
    def __init__(self, parent_ins, name_base, z1, z2, n):
        super().__init__(parent_ins, name_base)
        self.flag_ele_list = True
        self.add_child('1开路阻抗', TPortZParallel(self, '1开路阻抗', z2))
        self.add_child('2短路阻抗', TPortZSeries(self, '2短路阻抗', z1))
        # self.add_child('2开路阻抗', TPortZParallel(self, '2开路阻抗', z2))
        self.add_child('3变压器', TPortCircuitN(self, '3变压器', n))


########################################################################################################################

# 移频脉冲防雷变压器
class TcsrFLYPMC(TcsrTransformerOpenShort):
    def __init__(self, parent_ins, name_base, z1, z2, n):
        super().__init__(parent_ins, name_base, z1, z2, n)


# 移频脉冲防雷变压器
class TcsrELYPMC(TcsrTransformerOpenShort):
    def __init__(self, parent_ins, name_base, z1, z2, n):
        super().__init__(parent_ins, name_base, z1, z2, n)


########################################################################################################################

# 白俄TAD变压器
class TcsrTADBelarus(TcsrTransformerOpenShort):
    def __init__(self, parent_ins, name_base, z1, z2, n):
        super().__init__(parent_ins, name_base, z1, z2, n)


# 白俄隔离盒
class TcsrIsolationBelarus(ElePack):
    def __init__(self, parent_ins, name_base, z1, z2):
        super().__init__(parent_ins, name_base)
        self.flag_ele_list = True
        self.add_child('1串联电阻', TPortZSeries(self, '1串联电阻', z1))
        self.add_child('2并联电阻', TPortZParallel(self, '2并联电阻', z2))


########################################################################################################################

# 防雷变压器
class TcsrFL(TcsrTransformer):
    def __init__(self, parent_ins, name_base, z1, z2, n):
        super().__init__(parent_ins, name_base, z1, z2, n)


########################################################################################################################

# TAD变压器
class TcsrTAD(ElePack):
    def __init__(self, parent_ins, name_base, z1, z2, z3, n, zc):
        super().__init__(parent_ins, name_base)
        self.flag_ele_list = True
        self.add_child('1共模电感', TPortZSeries(self, '1共模电感', z3))
        self.add_child('2等效内阻', TPortCircuitT(self, '2等效内阻', z1, z2, z1))
        self.add_child('3变压器', TPortCircuitN(self, '3变压器', n))
        self.add_child('4串联电容', TPortZSeries(self, '4串联电容', zc))


########################################################################################################################

# 匹配单元
class TcsrBA(TPortZParallel):
    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base, z)

    def get_coeffs(self, freq):
        z = self.z[self.m_freq.value][freq].z
        self.value2coeffs(z)
        return self.equs

    @property
    def m_freq(self):
        return self.parent_ins.m_freq


########################################################################################################################

# 引接线
class TcsrCA(TPortZSeries):
    def __init__(self, parent_ins, name_base, z):
        super().__init__(parent_ins, name_base, z)


class TcsrCableComp(TPortZSeries):
    def __init__(self, parent_ins, name_base, z=45*9):
        super().__init__(parent_ins, name_base, z)

    def get_coeffs(self, freq):
        z = self.z
        self.value2coeffs(z)
        return self.equs
