# ==== Environment Variables ====
#     vvvv DO NOT CHANGE vvvv
include                       /nfs/wsi/es/tools/gnu/gmsl/gmsl
XCELIUM_BIN                := /nfs/wsi/es/tools/cadence/XCELIUM/22.09.007/tools/bin/xrun
XCELIUM_ELAB_FLAGS         := -coverage all -covoverwrite -abvevalnochange -64 -elaborate -v93 -sv -exit -access +rw -timescale '1ps/1fs' -vhdlsync -enable_tcl_tcheck_net -l xrun.log -append_log -nohistory -v200x -nowarn CSINFI -allowredefinition
XCELIUM_RUN_FLAGS          := -coverage all -covoverwrite -abvevalnochange -64 -access +rw -R -snapshot run -v93 -timescale '1ps/1fs' -vhdlsync -enable_tcl_tcheck_net -l xrun.log -append_log -nohistory -v200x -nowarn CSINFI -allowredefinition
SIMVISION_BIN              := /nfs/wsi/es/tools/cadence/XCELIUM/22.09.007/tools/bin/simvision
VMANAGER_BIN               := /nfs/wsi/es/tools/cadence/VMANAGER/23.09.002/bin/imc
GENUS_BIN                  := /nfs/wsi/es/tools/cadence/DDI/23.10.000/bin/genus
GENUS_FLAGS                := -common_ui
GENUS_DONT_USE             := HA* FA*
VITIS_BIN                  := /nfs/wsi/es/tools/xilinx/Vitis_HLS/2022.2/bin/vitis_hls
SYN_LIB_FILE               := /nfs/wsi/es/eda/Nangate/stdc/si2/instances/latest/liberty/CCS/NangateOpenCellLibrary_typical_ccs.lib
POST_SYN_GATE_FILE         := /nfs/wsi/es/eda/Nangate/stdc/si2/instances/latest/verilog/NangateOpenCellLibrary.v
LM_LICENSE_FILE            := 1701@menelaos.cs.uni-tuebingen.de
LOCAL_VARS_CADENCE         := $(strip $(foreach var, $(.VARIABLES), $(if $(filter command line, $(origin $(var))),-define $(var)=$($(var)),)))
export W3264_NO_HOST_CHECK := 1
export LM_LICENSE_FILE     := $(LM_LICENSE_FILE)
export MDV_XLM_HOME        := $(shell dirname $(shell dirname $(dir $(XCELIUM_BIN))))
.PHONY: help elaborate sdc xconf post_xconf env clean hls_conf sim_post_cleanup sim post_sim post_sim_post_cleanup hls_post_cleanup
#     ^^^^ DO NOT CHANGE ^^^^

#     vvvv CHANGE vvvv
# ==== Design Files ====
# --- Design Setup and Simulation related ---
# List source files here (not the testbench!).
HDL_SRC             := n_block_cbc_unrolled.v
# Put testbench file here!
HDL_TB_SRC          := tb_cbc_unrolled.sv
# Top module name for Simulation. If a testbench exits this should be the name of the testbench module.
HDL_TB_TOP          := tb_cbc

# --- Synthesis and Post-Synthesis related ---
# Top module name Synthesis.
HDL_SYN_TOP         := 
# Instance name of the Synthesis top module inside the testbench (for example: module_def # (<params>) i_dut (<port list>) endmodule => i_dut)
HDL_SYN_TOP_TB_INST := 

# --- Waveform generation related ---
# Name of the VCD file which is generated.
VCD_FN               := cbc.vcd

# --- High-Level-Synthesis related ---
# Put path to the HLS C/C++ source file
HLS_SRC              := cbc.cpp
# Top function name HLS.
HLS_FUNC_TOP         := n_block_cbc

# ==== Constraints ====
# Name of the Clock Port you can define multiple clocks but also have provide their periods.
CLK_NAME     := ap_clk
# Period in time unit TIME_UNIT
PERIOD       := 10
# Name of the Reset Port. Only a single reset port exists.
RST_NAME     := ap_rst
# one of [us, ns, ps, fs]
TIME_UNIT    := ns
#     ^^^^ CHANGE ^^^^

help:
	@echo " ___   ___  ___  ___   _  _       _                ®"
	@echo "|   \ / __|| __|/ __| | || | ___ | | _ __  ___  _ _ "
	@echo "| |) |\__ \| _| \__ \ | __ |/ -_)| || '_ \/ -_)| '_|"
	@echo "|___/ |___/|___||___/ |_||_|\___||_|| .__/\___||_|  "
	@echo "                                         |_|        "
	@echo "This scripts is part of the DSES lecture offered at "
	@echo "the University of Tuebingen. The script is provided "
	@echo "'AS IS', without warranty of any kind. Students are "
	@echo "allowed to modify the scripts to their needs but    "
	@echo "have to ensure correct functionality themselves.    "
	@echo "NOTE: MODIFIED SCRIPTS MIGHT LEAD TO WRONG BEHAVIOR!"
	@echo "                                                    "
	@echo "Help:                                               "
	@echo "=====                                               "
	@echo "      make help           Display this help message."
	@echo "                                                    "
	@echo "      ======= Pre-Synthesis Simulation =======      "
	@echo "                                                    "
	@echo "      make elaborate      Elaborate the given design"
	@echo "                          files and testbench.      "
	@echo "                                                    "
	@echo "      make xconf          Create Xcelium tcl command"
	@echo "                          file.                     "
	@echo "                                                    "
	@echo "      make sim            Elaborate and Simulate the"
	@echo "                          the given design and test-"
	@echo "                          bench files.              "
	@echo "                                                    "
	@echo "      make sim_gui        Elaborate and Simulate the"
	@echo "                          the given design and test-"
	@echo "                          bench files with GUI.     "
	@echo "                                                    "
	@echo "              ======= Coverage =======              "
	@echo "                                                    "
	@echo "      make coverage       Starts the tool with which"
	@echo "                          coverage reports can be   "
	@echo "                          opened.                   "
	@echo "                                                    "
	@echo "              ======= Synthesis =======             "
	@echo "                                                    "
	@echo "      make sdc            Create simple synthesis   "
	@echo "                          constraint file.          "
	@echo "                                                    "
	@echo "      make gconf          Create Genus tcl command  "
	@echo "                          file.                     "
	@echo "                                                    "
	@echo "      make synthesis      Synthesis the given design"
	@echo "                          files.                    "
	@echo "                                                    "
	@echo "      make synthesis_gui  Synthesis the given design"
	@echo "                          files with GUI (follow the"
	@echo "                          instructions printed to   "
	@echo "                          the standard output).     "
	@echo "      ======= Post-Synthesis Simulation =======     "
	@echo "                                                    "
	@echo "      make post_xconf     Create Xcelium post-syn   "
	@echo "                          tcl command file.         "
	@echo "                                                    "
	@echo "      make post_sim       Post-Synthesis simulation "
	@echo "                          of the synthesized design."
	@echo "                                                    "
	@echo "      make post_sim_gui   Post-Synthesis simulation "
	@echo "                          of the synthesized design."
	@echo "                          with GUI.                 "
	@echo "                                                    "
	@echo "         ======= High-Level-Synthesis =======       "
	@echo "                                                    "
	@echo "      make hls_conf       Create Vitis hls tcl      "
	@echo "                          command file.             "
	@echo "                                                    "
	@echo "      make hls            High-Level-Synthesis of   "
	@echo "                          the design.               "
	@echo "                                                    "
	@echo "      make hls_gui        High-Level-Synthesis of   "
	@echo "                          the design with GUI.      "
	@echo "                                                    "
	@echo "                 ======= Misc =======               "
	@echo "                                                    "
	@echo "      make env            Create a file containing  "
	@echo "                          environment variables.    "
	@echo "                          Compatible with bash, zsh!"
	@echo "                                                    "
	@echo "      make clean          Delete all files generated"
	@echo "                          by other targets.         "

#    ___  _____  _
#   | _ \|_   _|| |
#   |   /  | |  | |__
#   |_|_\  |_|  |____|
#

elaborate:
	@echo "-- Elaborate"
	@rm -rf sim
	@mkdir -p sim/logfiles
	$(XCELIUM_BIN) $(XCELIUM_ELAB_FLAGS) -xmlibdirname sim -top $(HDL_TB_TOP) $(HDL_SRC) $(HDL_TB_SRC) $(LOCAL_VARS_CADENCE)

xconf: elaborate
	@echo "-- TCL Command File for Xcelium"
	@echo "database -open vcddb -into $(VCD_FN) -vcd -default"               >  ./sim/xconf.tcl
	@echo "probe -name $(USER) -create -vcd -all -depth all -database vcddb" >> ./sim/xconf.tcl

sim: xconf
	@echo "-- Simulation"
	@echo "run"  >> ./sim/xconf.tcl
	@echo "exit" >> ./sim/xconf.tcl
	-$(XCELIUM_BIN) $(XCELIUM_RUN_FLAGS) -xmlibdirname sim -input ./sim/xconf.tcl $(LOCAL_VARS_CADENCE)
	@$(MAKE) sim_post_cleanup

sim_gui: xconf
	@echo "-- Simulation with GUI"
	@PATH=$(SIMVISION_BIN):$(PATH)
	-$(XCELIUM_BIN) $(XCELIUM_RUN_FLAGS) -xmlibdirname sim -input ./sim/xconf.tcl -gui $(LOCAL_VARS_CADENCE) 
	@$(MAKE) sim_post_cleanup

sim_post_cleanup:
	-@sed -i 's/$$version/$$comment\n\tSimVision SST: '"$(shell echo -n $$(whoami) | md5sum | awk '{print $$1}')"'\n$$end\n$$version/g' $(VCD_FN) 2>/dev/null
	-@mv xrun.log sim/logfiles
	-@mv $(VCD_FN) sim
	-@mv cov_work sim
	@rm -rf xrun.key .simvision *.shm

#    ___             _    _              _
#   / __| _  _  _ _ | |_ | |_   ___  ___(_) ___
#   \__ \| || || ' \|  _|| ' \ / -_)(_-<| |(_-<
#   |___/ \_, ||_||_|\__||_||_|\___|/__/|_|/__/
#         |__/

sdc:
	@mkdir -p synthesis
	@echo "-- SDC Constraint Files for GENUS" 
	@echo "set clks_def [list $(foreach idx, $(shell seq 1 $(words $(PERIOD))), $(word $(idx),$(CLK_NAME)) $(word $(idx),$(PERIOD)))]" > ./synthesis/constraints.sdc
	@echo "foreach {clk period} \$${clks_def}  {"                                                                                      >> ./synthesis/constraints.sdc
	@echo "  if {[get_port -quiet \$${clk}] != \"\"} {"                                                                                >> ./synthesis/constraints.sdc
	@echo "    set_units -time 1$(TIME_UNIT) -capacitance 1fF"                                                                         >> ./synthesis/constraints.sdc
	@echo "    create_clock -name \$${clk} -period \$${period} [get_port \$${clk}]"                                                    >> ./synthesis/constraints.sdc
	@echo "    set_input_delay -clock \$${clk} -max 2 [remove_from_collection [all_inputs] \$${clk}]"                                  >> ./synthesis/constraints.sdc
	@echo "    set_input_delay -clock \$${clk} -min 1 [remove_from_collection [all_inputs] \$${clk}]"                                  >> ./synthesis/constraints.sdc
	@echo "    set_output_delay -clock \$${clk} -max 2 [remove_from_collection [all_outputs] \$${clk}]"                                >> ./synthesis/constraints.sdc
	@echo "    set_output_delay -clock \$${clk} -min -1 [remove_from_collection [all_outputs] \$${clk}]"                               >> ./synthesis/constraints.sdc
	@echo "    if {\"$(RST_NAME)\" != \"\" && [get_port -quiet $(RST_NAME)] != \"\"} {"                                                >> ./synthesis/constraints.sdc
	@echo "      set_false_path -from [get_port $(RST_NAME)]"                                                                          >> ./synthesis/constraints.sdc
	@echo "    } else {"                                                                                                               >> ./synthesis/constraints.sdc
	@echo "      info \"Design might require reset port\""                                                                             >> ./synthesis/constraints.sdc
	@echo "    }"                                                                                                                      >> ./synthesis/constraints.sdc
	@echo "  }"                                                                                                                        >> ./synthesis/constraints.sdc
	@echo "}"                                                                                                                          >> ./synthesis/constraints.sdc
	@echo "if {[llength \$${clks_def}] > 2} {"                                                                                         >> ./synthesis/constraints.sdc
	@echo "  set_clock_groups $(foreach item, $(CLK_NAME), -group {$(item)})"                                                          >> ./synthesis/constraints.sdc
	@echo "}"                                                                                                                          >> ./synthesis/constraints.sdc

gsetup: sdc
	@echo "-- TCL Command File for GENUS"
	@echo "set_db source_verbose false"                                  > ./synthesis/gconf.tcl
	@echo "read_libs $(SYN_LIB_FILE)"                                    >> ./synthesis/gconf.tcl
	@echo "foreach f {$(HDL_SRC)} {"                                     >> ./synthesis/gconf.tcl
	@echo "  if { [string match *.vhd \$${f}] } {"                       >> ./synthesis/gconf.tcl
	@echo "    read_hdl -language vhdl \$${f} $(LOCAL_VARS_CADENCE)"     >> ./synthesis/gconf.tcl
	@echo "  } elseif { [string match *.v \$${f}] } {"                   >> ./synthesis/gconf.tcl
	@echo "    read_hdl -language v2001 \$${f} $(LOCAL_VARS_CADENCE)"    >> ./synthesis/gconf.tcl
	@echo "  } elseif { [string match *.svh \$${f}] } {"                 >> ./synthesis/gconf.tcl
	@echo "    read_hdl -language sv \$${f} $(LOCAL_VARS_CADENCE)"       >> ./synthesis/gconf.tcl
	@echo "  } elseif { [string match *.sv \$${f}] } {"                  >> ./synthesis/gconf.tcl
	@echo "    read_hdl -language sv \$${f} $(LOCAL_VARS_CADENCE)"       >> ./synthesis/gconf.tcl
	@echo "  }"                                                          >> ./synthesis/gconf.tcl
	@echo "}"                                                            >> ./synthesis/gconf.tcl
	@$(foreach du, $(GENUS_DONT_USE),\
		echo "set_dont_use \"$(du)\" true" >> ./synthesis/gconf.tcl ; \
	)

gconf: gsetup
	@echo "elaborate $(HDL_SYN_TOP)"                                                 >> ./synthesis/gconf.tcl
	@echo "read_sdc ./synthesis/constraints.sdc"                                     >> ./synthesis/gconf.tcl
	@echo "syn_generic"                                                              >> ./synthesis/gconf.tcl
	@echo "syn_map"                                                                  >> ./synthesis/gconf.tcl
	@echo "syn_opt"                                                                  >> ./synthesis/gconf.tcl
	@echo "report_power  > ./synthesis/report_power.rpt"                             >> ./synthesis/gconf.tcl
	@echo "report_gates  > ./synthesis/report_gate.rpt"                              >> ./synthesis/gconf.tcl
	@echo "report_area   > ./synthesis/report_area.rpt"                              >> ./synthesis/gconf.tcl
	@echo "foreach {clk} [list $(CLK_NAME)]  {"                                      >> ./synthesis/gconf.tcl
	@echo "  report_timing -group \$${clk} > ./synthesis/report_timing_\$${clk}.rpt" >> ./synthesis/gconf.tcl
	@echo "}"                                                                        >> ./synthesis/gconf.tcl
	@echo "report_timing -unconstrained > ./synthesis/report_utiming.rpt"            >> ./synthesis/gconf.tcl
	@echo "write_hdl $(HDL_SYN_TOP) > ./synthesis/syn_$(HDL_SYN_TOP).v"              >> ./synthesis/gconf.tcl
	@echo "exit"                                                                     >> ./synthesis/gconf.tcl

gconf_gui: gsetup
	@echo "gui_show"                                                                           >> ./synthesis/gconf.tcl
	@echo "puts \"\\[ESES TODO\\] ENTER THE FOLLOWING COMMANDS MANUALLY (without the \\\"):\"" >> ./synthesis/gconf.tcl
	@echo "puts \"-  elaborate $(HDL_SYN_TOP)\""                                               >> ./synthesis/gconf.tcl
	@echo "puts \"-  read_sdc ./synthesis/constraints.sdc\""                                   >> ./synthesis/gconf.tcl
	@echo "puts \"-  syn_generic\""                                                            >> ./synthesis/gconf.tcl
	@echo "puts \"-  syn_map\""                                                                >> ./synthesis/gconf.tcl
	@echo "puts \"-  syn_opt\""                                                                >> ./synthesis/gconf.tcl
	@echo "puts \"-  report_gates  > ./synthesis/report_gate.rpt\""                            >> ./synthesis/gconf.tcl
	@echo "puts \"-  report_area   > ./synthesis/report_area.rpt\""                            >> ./synthesis/gconf.tcl
	@echo "foreach {clk} [list $(CLK_NAME)]  {"                                                >> ./synthesis/gconf.tcl
	@echo "  report_timing -group \$${clk} > ./synthesis/report_timing_\$${clk}.rpt"           >> ./synthesis/gconf.tcl
	@echo "}"                                                                                  >> ./synthesis/gconf.tcl
	@echo "puts \"-  report_timing -unconstrained > ./synthesis/report_utiming.rpt\""          >> ./synthesis/gconf.tcl
	@echo "puts \"-  write_hdl $(HDL_SYN_TOP) > ./synthesis/syn_$(HDL_SYN_TOP).v\""            >> ./synthesis/gconf.tcl
	@echo "puts \"-  exit\""                                                                   >> ./synthesis/gconf.tcl

synthesis: gconf
	@echo "-- Synthesis"
	$(GENUS_BIN) $(GENUS_FLAGS) -files ./synthesis/gconf.tcl -log ./synthesis/genus
	@rm -rf ./fv ./synthesis/fv .*.tstamp
	@echo "// GENUS UID $(shell echo -n $$(whoami) | md5sum | awk '{print $$1}')" >> ./synthesis/syn_$(HDL_SYN_TOP).v

synthesis_gui: gconf_gui
	@echo "-- Synthesis"
	$(GENUS_BIN) $(GENUS_FLAGS) -files ./synthesis/gconf.tcl -log ./synthesis/genus
	@rm -rf ./fv ./synthesis/fv .*.tstamp
	@echo "// GENUS UID $(shell echo -n $$(whoami) | md5sum | awk '{print $$1}')" >> ./synthesis/syn_$(HDL_SYN_TOP).v

#    ___           _         ___
#   | _ \ ___  ___| |_  ___ / __| _  _  _ _
#   |  _// _ \(_-<|  _||___|\__ \| || || ' \
#   |_|  \___//__/ \__|     |___/ \_, ||_||_|
#                                 |__/

post_elaborate:
	@echo "-- Pre-Synthesis Elaborate"
	@rm -rf post_sim
	@mkdir -p post_sim/logfiles
	$(XCELIUM_BIN) $(XCELIUM_ELAB_FLAGS) -xmlibdirname post_sim -top $(HDL_TB_TOP) $(POST_SYN_GATE_FILE) ./synthesis/syn_$(HDL_SYN_TOP).v $(HDL_TB_SRC) -define SYNTHESIS $(LOCAL_VARS_CADENCE)

post_xconf: post_elaborate
	@echo "-- TCL Command File for Xcelium Post-Synthesis"
	@echo "database -open vcddb -into post_$(VCD_FN) -vcd -default"                  >  ./post_sim/post_xconf.tcl
	@echo "if {\"$(HDL_SYN_TOP_TB_INST)\" != \"\"} {"                                >> ./post_sim/post_xconf.tcl
	@echo "  tcheck $(HDL_TB_TOP).$(HDL_SYN_TOP_TB_INST) -on -type setup -depth all" >> ./post_sim/post_xconf.tcl
	@echo "  tcheck $(HDL_TB_TOP).$(HDL_SYN_TOP_TB_INST) -on -type hold -depth all"  >> ./post_sim/post_xconf.tcl
	@echo "}"                                                                        >> ./post_sim/post_xconf.tcl
	@echo "probe -create -vcd -all -depth all -database vcddb"                       >> ./post_sim/post_xconf.tcl
	@echo "set pack_assert_off {std_logic_arith numeric_std}"                        >> ./post_sim/post_xconf.tcl

post_sim: post_xconf
	@echo "-- Simulation Post-Synthesis"
	@echo "run"  >> ./post_sim/post_xconf.tcl
	@echo "exit" >> ./post_sim/post_xconf.tcl
	-$(XCELIUM_BIN) $(XCELIUM_RUN_FLAGS) -xmlibdirname post_sim -input ./post_sim/post_xconf.tcl -define SYNTHESIS $(LOCAL_VARS_CADENCE)
	@$(MAKE) post_sim_post_cleanup

post_sim_gui: post_xconf
	@echo "-- Simulation Post-Synthesis with GUI"
	-$(XCELIUM_BIN) $(XCELIUM_RUN_FLAGS) -xmlibdirname post_sim -input ./post_sim/post_xconf.tcl -gui -define SYNTHESIS $(LOCAL_VARS_CADENCE)
	@$(MAKE) post_sim_post_cleanup

post_sim_post_cleanup:
	-@sed -i 's/$$version/$$comment\n\tSimVision SST: '"$(shell echo -n $$(whoami) | md5sum | awk '{print $$1}')"'\n$$end\n$$version/g' post_$(VCD_FN) 2>/dev/null
	-@mv xrun.log post_sim/logfiles
	-@mv post_$(VCD_FN) post_sim
	@rm -rf xrun.key .simvision *.shm

#    _  _  _     ___
#   | || || |   / __|
#   | __ || |__ \__ \
#   |_||_||____||___/
#
hls_conf:
	@rm -rf hls
	@mkdir -p hls
	@echo "-- TCL Command File for Vitis HLS"
	@echo "cd hls"                                                                                                      >  ./hls/vconf.tcl
	@echo "open_project -reset vitis_hls"                                                                               >> ./hls/vconf.tcl
	@echo "set_top $(HLS_FUNC_TOP)"                                                                                     >> ./hls/vconf.tcl
	@echo "add_files ../$(HLS_SRC)"                                                                                     >> ./hls/vconf.tcl
	@echo "open_solution \"solution1\" -flow_target vivado"                                                             >> ./hls/vconf.tcl
	@echo "set_part {xc7vx485tffg1761-2}"                                                                               >> ./hls/vconf.tcl
	@echo "create_clock -period $(PERIOD)$(TIME_UNIT)"                                                                  >> ./hls/vconf.tcl
	@echo "csynth_design"                                                                                               >> ./hls/vconf.tcl
	@echo "export_design -format ip_catalog -display_name \"$(shell echo -n $$(whoami) | md5sum | awk '{print $$1}')\"" >> ./hls/vconf.tcl
	@echo "if {[file exist  vitis_hls/solution1/syn]} {"                                                                >> ./hls/vconf.tcl
	@echo "  file copy -force vitis_hls/solution1/syn ./"                                                               >> ./hls/vconf.tcl
	@echo "}"                                                                                                           >> ./hls/vconf.tcl

hls: hls_conf
	@echo "-- High-Level-Synthesis"
	-$(VITIS_BIN) ./hls/vconf.tcl
	@$(MAKE) hls_post_cleanup

hls_gui: hls_conf
	@echo "-- High-Level-Synthesis with GUI"
	-$(VITIS_BIN) -p ./hls/vconf.tcl
	@$(MAKE) hls_post_cleanup

hls_post_cleanup:
	-@echo "INFO: [HLS UID] $(shell echo -n $$(whoami) | md5sum | awk '{print $$1}')" >> vitis_hls.log
	@mv vitis_hls.log hls

#     ___                                             _____           _ 
#    / __| ___ __ __ ___  _ _  ___  __ _  __ _  ___  |_   _|___  ___ | |
#   | (__ / _ \\ V // -_)| '_|/ -_)/ _` |/ _` |/ -_)   | | / _ \/ _ \| |
#    \___|\___/ \_/ \___||_|  \___|\__,_|\__, |\___|   |_| \___/\___/|_|
#                                        |___/
coverage:
	@echo "-- Starting the Coverage Report Parsing Tool"
	@$(VMANAGER_BIN)
	@$(MAKE) coverage_post_cleanup

coverage_post_cleanup:
	@mkdir -p coverage
	@mv imc.log coverage
	@mv mdv.log coverage

#    __  __  _
#   |  \/  |(_) ___ __
#   | |\/| || |(_-</ _|
#   |_|  |_||_|/__/\__|
#
env:
	@echo "-- Environment File"
	@echo "export LM_LICENSE_FILE=$(LM_LICENSE_FILE)"                                                             >  env.sh
	@echo "export PATH=$$(dirname $(SIMVISION_BIN)):$$(dirname $(VITIS_BIN)):$$(dirname $(VMANAGER_BIN)):$$PATH)" >> env.sh
	@echo "export MDV_XLM_HOME=$(MDV_XLM_HOME)"                                                                   >> env.sh
	@echo "export W3264_NO_HOST_CHECK=1"                                                                          >> env.sh

clean:
	@echo "-- Clean"
	@rm -rf *.vcd \
          *.histroy \
          *.log \
          hls \
          xcelium.d \
          xrun.* \
          *.key \
          env.sh \
          xconf.tcl \
          post_xconf.tcl \
          syn_*.v \
          *.rpt \
          constraints.sdcs \
          gconf.tcl \
          genus.* \
          .*.tstamp \
          fv \
          synthesis \
          *.shm \
          .simvision \
          post_sim \
          sim \
          *.diag \
          *.mtarpt \
          cov_work \
          imc.log \
          coverage \
          mdv.log \
          .bpad \
          *.err
