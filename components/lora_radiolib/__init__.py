import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import CONF_ID, CONF_FREQUENCY

DEPENDENCIES = ['spi', 'text_sensor']

lora_ns = cg.esphome_ns.namespace('lora_radiolib')
# อัปเกรดคลาสให้สืบทอดคุณสมบัติของ TextSensor
LoRaRadioLib = lora_ns.class_('LoRaRadioLib', text_sensor.TextSensor, cg.Component)

CONF_CS_PIN = 'cs_pin'
CONF_DIO0_PIN = 'dio0_pin'
CONF_RST_PIN = 'rst_pin'

# บังคับว่าผู้ใช้ต้องตั้งชื่อ (name) ให้เซนเซอร์ตัวนี้ใน YAML ด้วย
CONFIG_SCHEMA = text_sensor.text_sensor_schema(LoRaRadioLib).extend({
    cv.Required(CONF_CS_PIN): cv.int_,
    cv.Required(CONF_DIO0_PIN): cv.int_,
    cv.Required(CONF_RST_PIN): cv.int_,
    cv.Optional(CONF_FREQUENCY, default=433.0): cv.float_,
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    cg.add_library("jgromes/RadioLib", "6.3.0")
    var = cg.new_Pvariable(config[CONF_ID])
    
    # ลงทะเบียนเป็นทั้งคอมโพเนนต์และเซนเซอร์
    await cg.register_component(var, config)
    await text_sensor.register_text_sensor(var, config)
    
    cg.add(var.set_pins(config[CONF_CS_PIN], config[CONF_DIO0_PIN], config[CONF_RST_PIN]))
    cg.add(var.set_frequency(config[CONF_FREQUENCY]))
