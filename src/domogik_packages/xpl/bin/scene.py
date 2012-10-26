#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import time
from domogik.xpl.common.xplconnector import Listener
from domogik.xpl.common.plugin import XplPlugin
from domogik.xpl.common.xplmessage import XplMessage
from domogik.xpl.common.queryconfig import Query
from domogik_packages.xpl.lib.scene import *
from urllib import *
import ConfigParser
import glob
from xml.dom import minidom
import threading
import ast
import os

class SceneManager(XplPlugin):
   """Plugin destine a faire de petite automatisation
   """
   sceneCount = 0
   globalscene=[]
   def __init__(self):
      XplPlugin.__init__(self, name = 'scene')
      print ("manager= %s" %self.myxpl)
      self.manager= self.myxpl
      print (self.manager)
      
      try:
          self.scene = Scene(self.log, self.send_xpl)
          self.log.info("Start Scene")
          self.scene.open()

      except SceneException as err:
          self.log.error(err.value)
          print(err.value)
          self.force_leave()
          return

      ### Start listening 
      try:
          self.log.info("Start listening to Scene")
          scene_listen = threading.Thread(None,
                                        self.scene.listen,
                                        None,
                                        (),
                                        {})
          scene_listen.start()
      except SceneException as err:
          self.log.error(err.value)
          print(err.value)
          self.force_leave()
          return


      ### Create listeners for commands
      self.log.info("Creating listener for KNX")
      Listener(self.scene_cmd, self.myxpl,{'schema':'scene.basic'})
      self.enable_hbeat()
      
      self.SceneCount = self.init_file()

      all_scene = self.scene.read_all(self.path)
      
      for scene in all_scene:
         self.mem_scene(all_scene[scene])

      self.log.info("Plugin ready :)")

   def init_file(self):
### init the file system
       self.path = self.get_data_files_directory()
       initfile = self.path+'init_scene.ini'      
       if os.path.exists(self.path) == False:
          os.mkdir(path, 0770)

       if os.path.exists(initfile)== False:
          file=ConfigParser.ConfigParser()
          file.add_section('Init')
          file.set('Init','number','0')
          number = 0
       else:
          file=ConfigParser.ConfigParser()
          file.read(initfile)
          number = file.get('Init','number')
       return number
      
   def mem_scene(self, scene):
### init scene one by one
      print(scene)
      devices={}
      actions={}
      for section in scene:
         if 'type' in scene[section]:
            if scene[section]['type']=='devices':
               devices[section]=scene[section]
            if scene[section]['type']=='Action True' or scene[section]['type']=='Action False':
               actions[section]=scene[section]
               
      Mini_scene = Mscene(scene['Scene'],self.manager,devices,actions,scene['Rinor']['addressport'],self.get_sanitized_hostname())

      if 'option_start' in scene:
         option_start=scene['option_start']
      else:
         option_start=True

      if option_start==True:
         Mini_scene.scene_start()

   def scene_cmd(self, message):
### function call when plugin receive a message
      if 'command' in message.data and 'data' in message.data:
         if message.data['command'] == 'Create':
            self.Create_scene_msg(message.data)
   
   def Create_scene_msg(self, data):
       devices = {}
       actions = {}
       data = data.replace('|','')
       data = data.replace(':',":'")
       data = data.replace(',',"',")
       data = "{" + data + "'}"
       data = ast.literal_eval(data)
       
       
       Scene_section = {'name':self.SceneCount}
       Scene_section['id'] = ''
       Scene_section['file'] = self.patch+'/scene'+ self.SceneCount + '.scn'
       Scene_section['description'] = 'description'
       Scene_section['condition'] = data['condition']
       
       for i in range(100):
          devices_text = "device" + i
          if devices_test in message.data:
             device = {}
             device['type'] = 'devices'
             device['adr'] = data[devices_text+'adr']
             device['id'] = data[devices_text+'id']
             device['key'] = data[devices_text+'key']
             device['tech'] = data[devices_text+'tech']
             device['op']= data[devices_text+'op']
             device['value']= data[devices_text+'val']
             if device1_tech != '' and device1_key !='':
                device['filters'] = self.search_filter(device1_tech, device1_key)
             devices[devices_text]= device
          action_text = 'action'+i
          
          if action_text in data:
             action = {}
             action['type'] = data[action_text+'type']
             action['address'] = data[action_text+'adr']
             action['command'] = data[action_text+'cmd']
             action['value']= data[action_text+'val']
             actions[action_text]= action

          Rinor = {'addressport':data['rinor']} 
          Other = {'run':data['start_run'], 'init_test':''}
          
          New_Scene = Mscene(scene,self.manager,devices,action,Rinor,self.get_sanitized_hostname())
          
          
   def vielle_fonction(self):

      if "data" in message.data:
          data = message.data['data']
          if message.data['data']!="Read all scene":
             data = data.replace('|','')
             data = data.replace(':',":'")
             data = data.replace(',',"',")
             data = "{" + data + "'}"
             data = ast.literal_eval(data)

          if "actiontrueval" in message.data:
              data['actiontrueval'] = data['actiontrueval'].replace("%#",",")
          if "actionfalseval" in message.data:
              data['actionfalseval'] = data['actionfalseval'].replace("%#",",")

          if message.data['command']=="Create" and message.data['scene'] =='0':
             if "actiontrueval" in message.data:
                 data['actiontrueval'] = data['actiontrueval'].replace("%#",",")
             if "actionfalseval" in message.data:
                 data['actionfalseval'] = data['actionfalseval'].replace("%#",",")
             new_scene=ConfigParser.ConfigParser()
             msg=''
             self.sceneCount = self.sceneCount + 1

             if 'scene' not in data:
                self.sceneC = self.sceneCount
             else:
                self.sceneC = message

             device1_id = ''
             device1_adr = ''
             device1_tech = ''
             device1_key = ''
             device1_op = ''
             device1_value = ''
             device2_id = ''
             device2_adr = ''
             device2_tech = ''
             device2_key = ''
             device2_op = ''
             device2_value = ''
             op_global = ''
             action_true_techno = ''
             action_true_adr = ''
             action_true_value = ''
             action_true_cmd = ''
             action_false_techno = ''
             action_false_adr = ''
             action_false_value = ''
             action_false_cmd = ''
             filter_device1 = ''
             filter_device2 = ''
             descrip=''
             rinor=data['rinorip']+":"+data['rinorport']
             print 'rinor:%s' %rinor
             if 'option_start' in data:
                option_start=data['option_start']
             else:
                option_start='true'
             if 'descrip' in data:
                descrip=data['descrip']
             else:
                descrip="pas de description"
             if 'device1id' in data and data['device1id'] != '':
                device1_adr = data['device1adr']
                device1_id = data['device1id']
                device1_key = data['device1key']
                device1_tech= data['device1tech']
                device1_key= data['device1key']
                if 'device1op' in data and data['device1op'] != '':
                   device1_op= data['device1op']
                   device1_value= data['device1val']

             if 'device2id' in data and data['device2id'] != '':
                device2_adr = data['device2adr']
                device2_id = data['device2id']
                device2_key = data['device2key']
                device2_tech= data['device2tech']
                device2_key= data['device2key']
                if 'device2op' in data and data['device2op']!='':
                   device2_op= data['device2op']
                   device2_value= data['device2val']

             if 'opglobal' in data and data['opglobal'] != '':
                op_global = data['opglobal']

             condition={'test1':device1_op, 'value1':device1_value,'test2':device2_op,'value2':device2_value,'test_global':op_global}

             if 'actiontrueadr' in data and data['actiontrueadr'] != '':
                action_true_techno = data['actiontruetech']
                action_true_adr = data['actiontrueadr']
                print "actrion_true_value = %s" %data['actiontrueval']
                action_true_value = data['actiontrueval']
                if 'actiontruecmd' in data:
                    action_true_cmd = data['actiontruecmd']

             action_true={'techno':action_true_techno,'address':action_true_adr, 'command':action_true_cmd,'value':action_true_value}

             if 'actionfalseadr' in data and data['actionfalseadr'] != '':
                action_false_techno = data['actionfalsetech']
                action_false_adr = data['actionfalseadr']
                action_false_value = data['actionfalseval']
                if 'actionfalsecmd' in data:
                    action_false_cmd = data['actionfalsecmd']

             action_false={'techno':action_false_techno,'address':action_false_adr, 'command':action_false_cmd,'value':action_false_value}
         
             if device1_tech != '' and device1_key !='':
                filter_device1 = self.search_filter(device1_tech, device1_key)
                print "filre: %s" %filter_device1
             if device2_tech != '' and device2_key != '':
                filter_device2 = self.search_filter(device2_tech, device2_key)

             device1 = {'address':device1_adr,'id':device1_id, 'key_stat':device1_key,'listener':filter_device1}
             device2 = {'address':device2_adr,'id':device2_id, 'key_stat':device2_key,'listener':filter_device2}
         
             print 'self.manager=%s' %self.manager
             Mini_scene = Mscene(self.sceneC,self.manager,device1,device2,condition,action_true,action_false,rinor,self.get_sanitized_hostname())
             msg="{'scene':'%s','device1':%s,'device2':%s,'condition':%s,'action_true':%s,'action_false':%s,'rinor':'%s','descrip':'%s','option_start':'%s'}\n" %(self.sceneC,device1,device2,condition,action_true,action_false,rinor,descrip,option_start)
             self.scene.add_scene(self.filetoopen,msg)
             print "message to file: %s" %msg
#         the_url="http://%s/base/device/add/name/%s/address/%s/usage_id/scene/description/scene_plugin/reference/Mscene" %(self.Mscene,self.Mscene)

             print "création d'une scene"
             msg=XplMessage()
             msg.set_schema('scene.basic')
             sender= "domogik-scene.%s" %self.get_sanitized_hostname()
             msg.set_source(sender)
             msg.set_type('xpl-trig')
             msg.add_data({'command':'Create-ack'})
             msg.add_data({'scene':'0'})
             scene_number= 'scene_%s OK' %self.sceneC
             msg.add_data({'data':scene_number})

             self.myxpl.send(msg)

             new_file=ConfigParser.ConfigParser()
             new_file.add_section('Scene')
             new_file.set('Scene', 'name',self.sceneC)
             new_file.set('Scene', 'id','')
             new_file.set('Scene', 'Description',descrip)

             new_file.add_section('Device1')
             new_file.set('Device1','name')
             new_file.set('Device1','id',device1_id)
             new_file.set('Device1','adr',device1_adr)
             new_file.set('Device1','tech',device1_tech)
             new_file.set('Device1','key',device1_key)
             new_file.set('Device1','op',device1_op)
             new_file.set('Device1','value',device1_value)
             new_file.set('Device1','filter',filter_device1)

             new_file.add_section('Test')
             new_file.set('Test','op_global',op_global)

             new_file.add_section('Device2')
             new_file.set('Device2','name','')
             new_file.set('Device2','id',device2_id)
             new_file.set('Device2','adr',device2_adr)
             new_file.set('Device2','tech',device2_tech)
             new_file.set('Device2','key',device2_key)
             new_file.set('Device2','op',device2_op)
             new_file.set('Device2','value',device2_value)
             new_file.set('Device2','filter',filter_device2)

             new_file.add_section('Rinor')
             new_file.set('Rinor','addressport',rinor)

             new_file.add_section('Action_True')
             new_file.set('Action_True','address',action_true_adr)
             new_file.set('Action_True','techno',action_true_techno)
             new_file.set('Action_True','command',action_true_cmd)
             new_file.set('Action_True','value',action_true_value)

             new_file.add_section('Action_False')
             new_file.set('Action_False','address', action_false_adr)
             new_file.set('Action_False','techno', action_false_techno)
             new_file.set('Action_False','command',action_false_cmd)
             new_file.set('Action_False','value', action_false_value)

             new_file.add_section('Other')
             new_file.set('Other','start_up',option_start)
             new_file.set('Other','stats','false')
             new_file.set('Other','Run','stop')

             if option_start=='true':
                Mini_scene.start()

             fullname=self.get_data_files_directory()+ "/scene%s.scn" %self.sceneC
             with open(fullname, 'w') as fich:
                new_file.write(fich)
             fich.close

          if message.data['command']=="Read" and message.data['scene'] =='0':
             mem = self.scene.read_scene(self.filetoopen)
             print('commande read')
             list_scene=""
             for i in range(len(mem)):
                liste=str(mem[i])
                print "maliste:%s" %liste
                if liste !='':
                   liste=ast.literal_eval(liste)
                   if 'scene' in liste:
                      scenee=liste['scene']
                   else:
                      scenee='None'
                   if 'descrip' in liste:
                      list_scene=list_scene+"Scene_"+scenee+" "+liste['descrip']+","
                   else:
                      list_scene=list_scene+"Scene_"+scenee+" Pas de description,"
             msg=XplMessage()
             msg.set_schema('scene.basic')
             sender= "domogik-scene.%s" %self.get_sanitized_hostname() 
             msg.set_source(sender)
             msg.set_type('xpl-trig')
             msg.add_data({'command':'Read-ack'})
             msg.add_data({'scene':'0'})
             msg.add_data({'data':list_scene})
             self.myxpl.send(msg)

          if message.data['command']=="Delete" and message.data['scene'] !='0':
             mem = self.scene.read_scene(self.filetoopen)
             list_scene=mem
             msg=XplMessage()
             msg.set_schema('scene.basic')
             sender= "domogik-scene.%s" %self.get_sanitized_hostname()
             msg.set_source(sender)
             msg.set_type('xpl-trig')
             msg.add_data({'command':'Delete-ack'})
             msg.add_data({'scene':'0'})
             scene_number= 'scene_%s OK' %self.sceneC
             msg.add_data({'data':list_scene})
             self.myxpl.send(msg)

      if "command" in message.data and message.type=="xpl-cmnd":
         print("Message recu contenant commande et xpl-cmdn")
 
         if message.data['command'] == "true" and message.type == "xpl-cmnd":
            print("Réception xpl cmnd true")
            msg=XplMessage()
            msg.set_schema('scene.basic')
            sender= "domogik-scene0.%s" %self.get_sanitized_hostname()
            msg.set_source(sender)
            msg.set_type('xpl-trig')
            msg.add_data({'number':message.data['number']})
            msg.add_data({'stats':'true'})
            self.myxpl.send(msg)
         if message.data['command']== "false" and message.type=="xpl-cmnd":
            print("Réceptino xpl cmnd false")
            msg=XplMessage()
            msg.set_schema('scene.basic')
            sender= "domogik-scene0.%s" %self.get_sanitized_hostname()
            msg.set_source(sender)
            msg.set_type('xpl-trig')
            msg.add_data({'number':message.data['number']})
            msg.add_data({'stats':'false'})
            self.myxpl.send(msg)

   def search_filter(self, techno, key_stat):
### open all xml file to find xpl schema and parametrer for create correct listerner
      device_list=[]
      filetoopen= self.get_stats_files_directory()
      filetoopen= filetoopen[:filetoopen.find('stats')+6]
      files = glob.glob("%s/*/*xml" % filetoopen)
      print "files récupérer"
      res = {}
      print "technologie: %s, key_stat: %s" %(techno,key_stat)
      for _files in files:
         if _files[-4:] == ".xml":
            doc = minidom.parse(_files)
            technology = doc.documentElement.attributes.get("technology").value
            schema_types = self.get_schemas_and_types(doc.documentElement)
            if technology not in res:
               res[technology] = {}
            for schema in schema_types:
               if schema not in res[technology]:
                  res[technology][schema] = {}
                  for xpl_type in schema_types[schema]:
                     if xpl_type == "xpl-trig" and technology == techno:
                        device, mapping, static_device, device_type = self.parse_mapping(doc.documentElement.getElementsByTagName("mapping")[0])
                        print "device: %s" %device
                        for i in range(len(mapping)):
                           print "keystat recherche %s, schema %s" %(mapping[i]['name'], schema)
                           print "mapping= %s" %mapping[i]
                           if "new_name" in mapping[i]:
                              if mapping[i]['new_name']==key_stat and schema not in device_list:
                                 test ={}
                                 test["schema"]="%s" %(schema)
                                 test["device"]="%s" %(device)
                                 test["xpl_stat"]="%s" %(mapping[i]['name'])
                                 device_list.append(test)
                           if mapping[i]['name']==key_stat and schema not in device_list:
                              test ={}
                              test["schema"]="%s" %(schema)
                              test["device"]="%s" %(device)
                              test["xpl_stat"]="%s" %(mapping[i]['name'])
                              device_list.append(test)
      return device_list

   def send_xpl(self):
      print("send xpl...")


   def get_schemas_and_types(self, node):
      """ Get the schema and the xpl message type
      @param node : the root (statistic) node
      @return {'schema1': ['type1','type2'], 'schema2', ['type1','type3']}
      """
      res = {}
      schemas = node.getElementsByTagName("schema")
      for schema in schemas:
          res[schema.attributes.get("name").value] = {}
          for xpltype in schema.getElementsByTagName("xpltype"):
              if xpltype.attributes.get("type").value == "*":
                  res[schema.attributes.get("name").value]["xpl-trig"] = xpltype
                  res[schema.attributes.get("name").value]["xpl-stat"] = xpltype
              else:
                  res[schema.attributes.get("name").value][xpltype.attributes.get("type").value] = xpltype
      return res

   def parse_mapping(self, node):
      """ Parse the "mapping" node
      """

      values = []
      device_node = node.getElementsByTagName("device")[0]
      device = None
      static_device = None
      device_type = None
      if device_node.attributes.has_key("field"):
          device = device_node.attributes["field"].value.lower()
      elif device_node.attributes.has_key("static_name"):
          static_device = device_node.attributes["static_name"].value.lower()
      elif device_node.attributes.has_key("type"):
          device_type = device_node.attributes["type"].value.lower()

      for value in node.getElementsByTagName("value"):
          name = value.attributes["field"].value
          data = {}
          data["name"] = name
          #If a "name" attribute is defined, use it as vallue, else value is empty
          if value.attributes.has_key("history_size"):
              data["history_size"] = int(value.attributes["history_size"].value)
          else:
              data["history_size"] = 0
          if value.attributes.has_key("new_name"):
              data["new_name"] = value.attributes["new_name"].value.lower()
              if value.attributes.has_key("filter_key"):
                  data["filter_key"] = value.attributes["filter_key"].value.lower()
                  if value.attributes.has_key("filter_value"):
                      data["filter_value"] = value.attributes["filter_value"].value.lower()
                  else:
                      data["filter_value"] = None
              else:
                  data["filter_key"] = None
                  data["filter_value"] = None
          else:
              data["new_name"] = None
              data["filter_key"] = None
              data["filter_value"] = None
          values.append(data)
      return device, values, static_device, device_type

if __name__ == "__main__":

   INST = SceneManager()