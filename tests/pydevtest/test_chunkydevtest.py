if (sys.version_info >= (2,7)):
import os, stat
        irodshome = "/"+irodszone+"/home/rods/"+s.adminsession.sessionId
        sfile2 = dir_w+"/sfile2"
        commands.getstatusoutput( "cat "+progname+" "+progname+" > "+sfile2 )
        myldir = dir_w+"/ldir"
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
        assertiCmd(s.adminsession,"imkdir icmdtest")
        
        assertiCmd(s.adminsession,"iinit -l", "LIST", s.adminsession.getUserName() )
        assertiCmd(s.adminsession,"iinit -l", "LIST", s.adminsession.getZoneName() )
        assertiCmd(s.adminsession,"iinit -l", "LIST", s.adminsession.getDefResource() )
        assert (res[0].count('NOTICE: irodsHost') == 1
                and res[0].count('NOTICE: irodsPort') == 1
                and res[0].count('NOTICE: irodsDefResource') == 1)
    
        assertiCmd(s.adminsession,"ilsresc", "LIST", self.testresc)
        assertiCmd(s.adminsession,"ilsresc -l", "LIST", self.testresc)
        assertiCmd(s.adminsession,"imiscsvrinfo", "LIST", ["relVersion"] )
        assertiCmd(s.adminsession,"iuserinfo", "LIST", "name: "+username )
        assertiCmd(s.adminsession,"ienv", "LIST", "irodsZone" )
        assertiCmd(s.adminsession,"ipwd", "LIST", "home" )
        assertiCmd(s.adminsession,"ihelp ils", "LIST", "ils" )
        assertiCmd(s.adminsession,"ierror -14000", "LIST", "SYS_API_INPUT_ERR" )
        assertiCmd(s.adminsession,"iexecmd hello", "LIST", "Hello world" )
        assertiCmd(s.adminsession,"ips -v", "LIST", "ips" )
        assertiCmd(s.adminsession,"iqstat", "LIST", "No delayed rules pending for user rods" )
    
        assertiCmd(s.adminsession,"ils -AL","LIST","home") # debug
        assertiCmd(s.adminsession,"iput -K --wlock "+progname+" "+irodshome+"/icmdtest/foo1" )
        assertiCmd(s.adminsession,"ichksum -f "+irodshome+"/icmdtest/foo1", "LIST", "performed = 1" )
        assertiCmd(s.adminsession,"iput -kf "+progname+" "+irodshome+"/icmdtest/foo1" )
        assertiCmd(s.adminsession,"ils "+irodshome+"/icmdtest/foo1" , "LIST", "foo1" )
        assertiCmd(s.adminsession,"ils -l "+irodshome+"/icmdtest/foo1", "LIST", ["foo1",myssize] )
        assertiCmd(s.adminsession,"iadmin ls "+irodshome+"/icmdtest", "LIST", "foo1" )
        assertiCmd(s.adminsession,"ils -A "+irodshome+"/icmdtest/foo1", "LIST", username+"#"+irodszone+":own" )
        assertiCmd(s.adminsession,"ichmod read "+testuser1+" "+irodshome+"/icmdtest/foo1" )
        assertiCmd(s.adminsession,"ils -A "+irodshome+"/icmdtest/foo1", "LIST", testuser1+"#"+irodszone+":read" )
        assertiCmd(s.adminsession,"irepl -B -R "+self.testresc+" --rlock "+irodshome+"/icmdtest/foo1" )
        assertiCmd(s.adminsession,"ils -l "+irodshome+"/icmdtest/foo1", "LIST", self.testresc )
    
        assertiCmd(s.adminsession,"itrim -S "+irodsdefresource+" -N1 "+irodshome+"/icmdtest/foo1" )
        assertiCmdFail(s.adminsession,"ils -L "+irodshome+"/icmdtest/foo1", "LIST", irodsdefresource )
        assertiCmd(s.adminsession,"iphymv -R "+irodsdefresource+" "+irodshome+"/icmdtest/foo1" )
        assertiCmd(s.adminsession,"ils -l "+irodshome+"/icmdtest/foo1", "LIST", irodsdefresource[0:19] )
        assertiCmd(s.adminsession,"imeta add -d "+irodshome+"/icmdtest/foo1 testmeta1 180 cm" )
        assertiCmd(s.adminsession,"imeta ls -d "+irodshome+"/icmdtest/foo1", "LIST", ["testmeta1"] )
        assertiCmd(s.adminsession,"imeta ls -d "+irodshome+"/icmdtest/foo1", "LIST", ["180"] )
        assertiCmd(s.adminsession,"imeta ls -d "+irodshome+"/icmdtest/foo1", "LIST", ["cm"] )
        assertiCmd(s.adminsession,"icp -K -R "+self.testresc+" "+irodshome+"/icmdtest/foo1 "+irodshome+"/icmdtest/foo2" )
        
        imeta_popen = subprocess.Popen('echo "ls -d ' + irodshome + '/icmdtest/foo1" | imeta -v', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        
        assertiCmd(s.adminsession,"iget -fK --rlock "+irodshome+"/icmdtest/foo2 /tmp/" )
        os.unlink( "/tmp/foo2" )
        
        assertiCmd(s.adminsession,"ils "+irodshome+"/icmdtest/foo2", "LIST", "foo2" )
        assertiCmd(s.adminsession,"imv "+irodshome+"/icmdtest/foo2 "+irodshome+"/icmdtest/foo4" )
        assertiCmd(s.adminsession,"ils -l "+irodshome+"/icmdtest/foo4", "LIST", "foo4" )
        assertiCmd(s.adminsession,"imv "+irodshome+"/icmdtest/foo4 "+irodshome+"/icmdtest/foo2" )
        assertiCmd(s.adminsession,"ils -l "+irodshome+"/icmdtest/foo2", "LIST", "foo2" )
        assertiCmd(s.adminsession,"ichksum "+irodshome+"/icmdtest/foo2", "LIST", "foo2" )
        assertiCmd(s.adminsession,"imeta add -d "+irodshome+"/icmdtest/foo2 testmeta1 180 cm" )
        assertiCmd(s.adminsession,"imeta add -d "+irodshome+"/icmdtest/foo1 testmeta2 hello" )
        assertiCmd(s.adminsession,"imeta ls -d "+irodshome+"/icmdtest/foo1", "LIST", ["testmeta1"] )
        assertiCmd(s.adminsession,"imeta ls -d "+irodshome+"/icmdtest/foo1", "LIST", ["hello"] )
        assertiCmd(s.adminsession,"imeta qu -d testmeta1 = 180", "LIST", "foo1" )
        assertiCmd(s.adminsession,"imeta qu -d testmeta2 = hello", "LIST", "dataObj: foo1" )
        assertiCmd(s.adminsession,"iget -f -K --rlock "+irodshome+"/icmdtest/foo2 "+dir_w )
        assert myssize == str(os.stat(dir_w+"/foo2").st_size)
        os.unlink( dir_w+"/foo2" )
    
    
        os.unlink( sfile2 )
    
    
    
    
    
    
    
        irodshome = "/"+irodszone+"/home/rods/"+s.adminsession.sessionId
        sfile2 = dir_w+"/sfile2"
        commands.getstatusoutput( "cat "+progname+" "+progname+" > "+sfile2 )
        myldir = dir_w+"/ldir"
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
        assertiCmd(s.adminsession,"imkdir icmdtest")
    
    
            mysfile = mysdir+"/sfile"+str(i)
            shutil.copyfile( progname, mysfile )
    
        assertiCmd(s.adminsession,"iput -K --wlock "+progname+" "+irodshome+"/icmdtest/foo1" )
        assertiCmd(s.adminsession,"icp -K -R "+self.testresc+" "+irodshome+"/icmdtest/foo1 "+irodshome+"/icmdtest/foo2" )
    
        assertiCmd(s.adminsession,"irepl -B -R "+self.testresc+" "+irodshome+"/icmdtest/foo1" )
        phypath = dir_w+"/"+"foo1."+str(random.randrange(10000000))
        assertiCmd(s.adminsession,"iput -kfR "+irodsdefresource+" "+sfile2+" "+irodshome+"/icmdtest/foo1" )
        assertiCmd(s.adminsession,"ils -l "+irodshome+"/icmdtest/foo1", "LIST", ["foo1",myssize] )
        assertiCmd(s.adminsession,"ils -l "+irodshome+"/icmdtest/foo1", "LIST", ["foo1",str(os.stat(sfile2).st_size)] )
        assertiCmd(s.adminsession,"irepl -U "+irodshome+"/icmdtest/foo1" )
        assertiCmdFail(s.adminsession,"ils -l "+irodshome+"/icmdtest/foo1", "LIST", myssize )
        assertiCmd(s.adminsession,"itrim -S "+irodsdefresource+" "+irodshome+"/icmdtest/foo1" )
        assertiCmd(s.adminsession,"iput -bIvPKr "+mysdir+" "+irodshome+"/icmdtest", "LIST", "Bulk upload" )
        rsfile = dir_w+"/rsfile"
        if os.path.isfile( rsfile ):
            os.unlink( rsfile )
        assertiCmd(s.adminsession,"iput -PkITr -X "+rsfile+" --retries 10 "+mysdir+" "+irodshome+"/icmdtestw", "LIST", "Processing" )
        assertiCmd(s.adminsession,"imv "+irodshome+"/icmdtestw "+irodshome+"/icmdtestw1" )
        assertiCmd(s.adminsession,"ils -lr "+irodshome+"/icmdtestw1", "LIST", "sfile10" )
        assertiCmd(s.adminsession,"ils -Ar "+irodshome+"/icmdtestw1", "LIST", "sfile10" )
        assertiCmd(s.adminsession,"irm -rvf "+irodshome+"/icmdtestw1", "LIST", "num files done" )
        if os.path.isfile( rsfile ):
            os.unlink( rsfile )
        assertiCmd(s.adminsession,"iget -vIKPfr -X rsfile --retries 10 "+irodshome+"/icmdtest "+dir_w+"/testx", "LIST", "opened" )
        if os.path.isfile( rsfile ):
            os.unlink( rsfile )
        commands.getstatusoutput( "tar -chf "+dir_w+"/testx.tar -C "+dir_w+"/testx ." )
        assertiCmd(s.adminsession,"iput "+dir_w+"/testx.tar "+irodshome+"/icmdtestx.tar" )
        assertiCmd(s.adminsession,"ibun -x "+irodshome+"/icmdtestx.tar "+irodshome+"/icmdtestx" )
        assertiCmd(s.adminsession,"ils -lr "+irodshome+"/icmdtestx", "LIST", ["foo2"] )
        assertiCmd(s.adminsession,"ils -lr "+irodshome+"/icmdtestx", "LIST", ["sfile10"] )
        assertiCmd(s.adminsession,"ibun -cDtar "+irodshome+"/icmdtestx1.tar "+irodshome+"/icmdtestx" )
        assertiCmd(s.adminsession,"ils -l "+irodshome+"/icmdtestx1.tar", "LIST", "testx1.tar" )
        if os.path.exists(dir_w+"/testx1"):
            shutil.rmtree(dir_w+"/testx1")
        os.mkdir( dir_w+"/testx1" )
        if os.path.isfile( dir_w+"/testx1.tar" ):
            os.unlink( dir_w+"/testx1.tar" )
        assertiCmd(s.adminsession,"iget "+irodshome+"/icmdtestx1.tar "+dir_w+"/testx1.tar" )
        commands.getstatusoutput( "tar -xvf "+dir_w+"/testx1.tar -C "+dir_w+"/testx1" )
        output = commands.getstatusoutput( "diff -r "+dir_w+"/testx "+dir_w+"/testx1/icmdtestx" )
        print "output is ["+str(output)+"]"
    
        assertiCmd(s.adminsession,"ibun -cDgzip "+irodshome+"/icmdtestx1.tar.gz "+irodshome+"/icmdtestx" )
        assertiCmd(s.adminsession,"ibun -x "+irodshome+"/icmdtestx1.tar.gz "+irodshome+"/icmdtestgz")
        if os.path.isfile( "icmdtestgz" ):
            os.unlink( "icmdtestgz" )
        assertiCmd(s.adminsession,"iget -vr "+irodshome+"/icmdtestgz "+dir_w+"", "LIST", "icmdtestgz")
        output = commands.getstatusoutput( "diff -r "+dir_w+"/testx "+dir_w+"/icmdtestgz/icmdtestx" )
        print "output is ["+str(output)+"]"
        shutil.rmtree( dir_w+"/icmdtestgz")
        assertiCmd(s.adminsession,"ibun --add "+irodshome+"/icmdtestx1.tar.gz "+irodshome+"/icmdtestgz")
        assertiCmd(s.adminsession,"irm -rf "+irodshome+"/icmdtestx1.tar.gz "+irodshome+"/icmdtestgz")
    
        assertiCmd(s.adminsession,"ibun -cDbzip2 "+irodshome+"/icmdtestx1.tar.bz2 "+irodshome+"/icmdtestx")
        assertiCmd(s.adminsession,"ibun -xb "+irodshome+"/icmdtestx1.tar.bz2 "+irodshome+"/icmdtestbz2")
        if os.path.isfile( "icmdtestbz2" ):
            os.unlink( "icmdtestbz2" )
        assertiCmd(s.adminsession,"iget -vr "+irodshome+"/icmdtestbz2 "+dir_w+"", "LIST", "icmdtestbz2")
        output = commands.getstatusoutput( "diff -r "+dir_w+"/testx "+dir_w+"/icmdtestbz2/icmdtestx" )
        print "output is ["+str(output)+"]"
        shutil.rmtree( dir_w+"/icmdtestbz2" )
        assertiCmd(s.adminsession,"irm -rf "+irodshome+"/icmdtestx1.tar.bz2")
        assertiCmd(s.adminsession,"iphybun -R "+self.anotherresc+" -Dbzip2 "+irodshome+"/icmdtestbz2" )
        assertiCmd(s.adminsession,"itrim -N1 -S "+self.testresc+" -r "+irodshome+"/icmdtestbz2", "LIST", "Total size trimmed" )
        assertiCmd(s.adminsession,"itrim -N1 -S "+irodsdefresource+" -r "+irodshome+"/icmdtestbz2", "LIST", "Total size trimmed" )
    
        output = commands.getstatusoutput( "ils -L "+irodshome+"/icmdtestbz2/icmdtestx/foo1 | tail -n1 | awk '{ print $NF }'")
        assertiCmd(s.adminsession,"ils --bundle "+bunfile, "LIST", "Subfiles" )
        assertiCmd(s.adminsession,"irm -rf "+irodshome+"/icmdtestbz2")
        assertiCmd(s.adminsession,"irm -f --empty "+bunfile )
    
        os.unlink( dir_w+"/testx1.tar" )
        os.unlink( dir_w+"/testx.tar" )
        shutil.rmtree( dir_w+"/testx1" )
        shutil.rmtree( dir_w+"/testx" )
        os.unlink( sfile2 )
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
        if os.path.exists( mysdir ):
            shutil.rmtree( mysdir )
    
    
    
    
    
        irodshome = "/"+irodszone+"/home/rods/"+s.adminsession.sessionId
        sfile2 = dir_w+"/sfile2"
        commands.getstatusoutput( "cat "+progname+" "+progname+" > "+sfile2 )
        myldir = dir_w+"/ldir"
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
        assertiCmd(s.adminsession,"imkdir icmdtest")
    
            mysfile = mysdir+"/sfile"+str(i)
            shutil.copyfile( progname, mysfile )
    
    
        commands.getstatusoutput( "mv "+sfile2+" /tmp/sfile2" )
        commands.getstatusoutput( "cp /tmp/sfile2 /tmp/sfile2r" )
        assertiCmd(s.adminsession,"ireg -KR "+self.testresc+" /tmp/sfile2 "+irodshome+"/foo5" ) # <-- FAILING - REASON FOR SKIPPING
        commands.getstatusoutput( "cp /tmp/sfile2 /tmp/sfile2r" )
        assertiCmd(s.adminsession,"ireg -KR "+self.anotherresc+" --repl /tmp/sfile2r  "+irodshome+"/foo5" )
        assertiCmd(s.adminsession,"iget -fK "+irodshome+"/foo5 "+dir_w+"/foo5" )
        output = commands.getstatusoutput("diff /tmp/sfile2  "+dir_w+"/foo5")
        print "output is ["+str(output)+"]"
        assertiCmd(s.adminsession,"ireg -KCR "+self.testresc+" "+mysdir+" "+irodshome+"/icmdtesta" )
        if os.path.exists(dir_w+"/testa"):
            shutil.rmtree( dir_w+"/testa" )
        assertiCmd(s.adminsession,"iget -fvrK "+irodshome+"/icmdtesta "+dir_w+"/testa", "LIST", "testa" )
        output = commands.getstatusoutput("diff -r "+mysdir+" "+dir_w+"/testa" )
        print "output is ["+str(output)+"]"
        shutil.rmtree( dir_w+"/testa" )
        testuser2home = "/"+irodszone+"/home/"+s.sessions[2].getUserName()
        commands.getstatusoutput( "cp /tmp/sfile2 /tmp/sfile2c" )
        assertiCmd(s.sessions[2],"ireg -KR "+self.testresc+" /tmp/sfile2c "+testuser2home+"/foo5", "ERROR", "PATH_REG_NOT_ALLOWED" )
        assertiCmd(s.sessions[2],"iput -R "+self.testresc+" /tmp/sfile2c "+testuser2home+"/foo5" )
        assertiCmd(s.sessions[2],"irm -f "+testuser2home+"/foo5" )
    
        os.unlink( "/tmp/sfile2c" )
        os.unlink( dir_w+"/foo5" )

        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
        if os.path.exists( mysdir ):
            shutil.rmtree( mysdir )
    
    
    
    
    
    
    
    
    
    
    
    
        irodshome = "/"+irodszone+"/home/rods/"+s.adminsession.sessionId
        sfile2 = dir_w+"/sfile2"
        commands.getstatusoutput( "cat "+progname+" "+progname+" > "+sfile2 )
        myldir = dir_w+"/ldir" 
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
    
    
            mysfile = mysdir+"/sfile"+str(i)
            shutil.copyfile( progname, mysfile )
    
    
        assertiCmd(s.adminsession,"imkdir icmdtest")
        assertiCmd(s.adminsession,"iput -K --wlock "+progname+" "+irodshome+"/icmdtest/foo1" )
        assertiCmd(s.adminsession,"icp -K -R "+self.testresc+" "+irodshome+"/icmdtest/foo1 "+irodshome+"/icmdtest/foo2" )
    
        assertiCmd(s.adminsession,"ireg -KCR "+self.testresc+" "+mysdir+" "+irodshome+"/icmdtesta" )
    
        assertiCmd(s.adminsession,"imcoll -m link "+irodshome+"/icmdtesta "+irodshome+"/icmdtestb" )
        assertiCmd(s.adminsession,"ils -lr "+irodshome+"/icmdtestb", "LIST", "icmdtestb" )
        if os.path.exists(dir_w+"/testb"):
            shutil.rmtree( dir_w+"/testb" )
        assertiCmd(s.adminsession,"iget -fvrK "+irodshome+"/icmdtestb "+dir_w+"/testb", "LIST", "testb" )
        output = commands.getstatusoutput("diff -r "+mysdir+" "+dir_w+"/testb" )
        print "output is ["+str(output)+"]"
        assertiCmd(s.adminsession,"imcoll -U "+irodshome+"/icmdtestb" )
        assertiCmd(s.adminsession,"irm -rf "+irodshome+"/icmdtestb" )
        shutil.rmtree( dir_w+"/testb" )
        assertiCmd(s.adminsession,"imkdir "+irodshome+"/icmdtestm" )
        assertiCmd(s.adminsession,"imcoll -m filesystem -R "+self.testresc+" "+mysdir+" "+irodshome+"/icmdtestm" )
        assertiCmd(s.adminsession,"imkdir "+irodshome+"/icmdtestm/testmm" )
        assertiCmd(s.adminsession,"iput "+progname+" "+irodshome+"/icmdtestm/testmm/foo1" )
        assertiCmd(s.adminsession,"iput "+progname+" "+irodshome+"/icmdtestm/testmm/foo11" )
        assertiCmd(s.adminsession,"imv "+irodshome+"/icmdtestm/testmm/foo1 "+irodshome+"/icmdtestm/testmm/foo2" )
        assertiCmd(s.adminsession,"imv "+irodshome+"/icmdtestm/testmm "+irodshome+"/icmdtestm/testmm1" )
    
        assertiCmd(s.adminsession,"imv "+irodshome+"/icmdtestm/testmm1/foo2 "+irodshome+"/icmdtest/foo100" )
        assertiCmd(s.adminsession,"ils -l "+irodshome+"/icmdtest/foo100", "LIST", "foo100" )
        assertiCmd(s.adminsession,"imv "+irodshome+"/icmdtestm/testmm1 "+irodshome+"/icmdtest/testmm1" )
        assertiCmd(s.adminsession,"ils -lr "+irodshome+"/icmdtest/testmm1", "LIST", "foo11" )
        assertiCmd(s.adminsession,"irm -rf "+irodshome+"/icmdtest/testmm1 "+irodshome+"/icmdtest/foo100" )
        if os.path.exists(dir_w+"/testm"):
            shutil.rmtree( dir_w+"/testm" )
        assertiCmd(s.adminsession,"iget -fvrK "+irodshome+"/icmdtesta "+dir_w+"/testm", "LIST", "testm")
        output = commands.getstatusoutput("diff -r "+mysdir+" "+dir_w+"/testm" )
        print "output is ["+str(output)+"]"
        assertiCmd(s.adminsession,"imcoll -U "+irodshome+"/icmdtestm" )
        assertiCmd(s.adminsession,"irm -rf "+irodshome+"/icmdtestm" )
        shutil.rmtree( dir_w+"/testm" )
        assertiCmd(s.adminsession,"imkdir "+irodshome+"/icmdtestt_mcol" )
        assertiCmd(s.adminsession,"ibun -c "+irodshome+"/icmdtestx.tar "+irodshome+"/icmdtest" ) # added so icmdtestx.tar exists
        assertiCmd(s.adminsession,"imcoll -m tar "+irodshome+"/icmdtestx.tar "+irodshome+"/icmdtestt_mcol" )
        assertiCmd(s.adminsession,"ils -lr "+irodshome+"/icmdtestt_mcol", "LIST", ["foo2"] )
        assertiCmd(s.adminsession,"ils -lr "+irodshome+"/icmdtestt_mcol", "LIST", ["foo1"] )
        if os.path.exists(dir_w+"/testt"):
            shutil.rmtree( dir_w+"/testt" )
        if os.path.exists(dir_w+"/testx"):
            shutil.rmtree( dir_w+"/testx" )
        assertiCmd(s.adminsession,"iget -vr "+irodshome+"/icmdtest  "+dir_w+"/testx", "LIST", "testx" )
        assertiCmd(s.adminsession,"iget -vr "+irodshome+"/icmdtestt_mcol/icmdtest  "+dir_w+"/testt", "LIST", "testt" )
        output = commands.getstatusoutput("diff -r  "+dir_w+"/testx "+dir_w+"/testt" )
        print "output is ["+str(output)+"]"
        assertiCmd(s.adminsession,"imkdir "+irodshome+"/icmdtestt_mcol/mydirtt" )
        assertiCmd(s.adminsession,"iput "+progname+" "+irodshome+"/icmdtestt_mcol/mydirtt/foo1mt" )
        assertiCmd(s.adminsession,"imv "+irodshome+"/icmdtestt_mcol/mydirtt/foo1mt "+irodshome+"/icmdtestt_mcol/mydirtt/foo1mtx" )
    
        assertiCmd(s.adminsession,"imcoll -U "+irodshome+"/icmdtestt_mcol" )
    
    
        os.unlink( sfile2 )
        shutil.rmtree( dir_w+"/testt" )
        shutil.rmtree( dir_w+"/testx" )
        if os.path.exists( mysdir ):
            shutil.rmtree( mysdir )
    
    
    
    
    
    
    
    
    
        irodshome = "/"+irodszone+"/home/rods/"+s.adminsession.sessionId
        sfile2 = dir_w+"/sfile2"
        commands.getstatusoutput( "cat "+progname+" "+progname+" > "+sfile2 )
        myldir = dir_w+"/ldir"
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
        assertiCmd(s.adminsession,"imkdir icmdtest")
    
    
        assertiCmd(s.adminsession,"iput -K --wlock "+progname+" "+irodshome+"/icmdtest/foo1" )
        assertiCmd(s.adminsession,"icp -K -R "+self.testresc+" "+irodshome+"/icmdtest/foo1 "+irodshome+"/icmdtest/foo2" )
    
        assertiCmd(s.adminsession,"ibun -c "+irodshome+"/icmdtestx.tar "+irodshome+"/icmdtest" ) # added so icmdtestx.tar exists
        assertiCmd(s.adminsession,"imkdir "+irodshome+"/icmdtestt_large" )
        assertiCmd(s.adminsession,"imcoll -m tar "+irodshome+"/icmdtestx.tar "+irodshome+"/icmdtestt_large" )
        assertiCmd(s.adminsession,"imkdir "+irodshome+"/icmdtestt_large/mydirtt" )
    
    
        lfile = dir_w+"/lfile"
        lfile1 = dir_w+"/lfile1"
        commands.getstatusoutput( "echo 012345678901234567890123456789012345678901234567890123456789012 > "+lfile )
            commands.getstatusoutput( "cat "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" > "+lfile1 )
            os.rename ( lfile1, lfile )
        os.mkdir( myldir )
        for i in range(1,3):
            mylfile = myldir+"/lfile"+str(i)
            mysfile = myldir+"/sfile"+str(i)
                shutil.copyfile( lfile, mylfile )
                os.rename( lfile, mylfile )
            shutil.copyfile( progname, mysfile )
    
        assertiCmd(s.adminsession,"iput "+myldir+"/lfile1 "+irodshome+"/icmdtestt_large/mydirtt" )
        assertiCmd(s.adminsession,"iget "+irodshome+"/icmdtestt_large/mydirtt/lfile1 "+dir_w+"/testt" )
        assertiCmd(s.adminsession,"irm -rf "+irodshome+"/icmdtestt_large/mydirtt" )
        assertiCmd(s.adminsession,"imcoll -s "+irodshome+"/icmdtestt_large" )
        assertiCmd(s.adminsession,"imcoll -p "+irodshome+"/icmdtestt_large" )
        assertiCmd(s.adminsession,"imcoll -U "+irodshome+"/icmdtestt_large" )
        assertiCmd(s.adminsession,"irm -rf "+irodshome+"/icmdtestt_large" )
        os.unlink( dir_w+"/testt" )
    
        os.unlink( sfile2 )
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        irodshome = "/"+irodszone+"/home/rods/"+s.adminsession.sessionId
        sfile2 = dir_w+"/sfile2"
        commands.getstatusoutput( "cat "+progname+" "+progname+" > "+sfile2 )
        myldir = dir_w+"/ldir"
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
        assertiCmd(s.adminsession,"imkdir icmdtest")
    
            mysfile = mysdir+"/sfile"+str(i)
            shutil.copyfile( progname, mysfile )
    
        assertiCmd(s.adminsession,"iput -rR "+self.testresc+" "+mysdir+" "+irodshome+"/icmdtestp" )
        assertiCmd(s.adminsession,"iphybun -KR "+self.anotherresc+" "+irodshome+"/icmdtestp" )
        assertiCmd(s.adminsession,"itrim -rS "+self.testresc+" -N1 "+irodshome+"/icmdtestp", "LIST", "files trimmed" )
        output = commands.getstatusoutput( "ils -L "+irodshome+"/icmdtestp/sfile1 | tail -n1 | awk '{ print $NF }'")
        assertiCmd(s.adminsession,"irepl --purgec -R "+self.anotherresc+" "+bunfile )
        assertiCmd(s.adminsession,"itrim -rS "+self.testresc+" -N1 "+irodshome+"/icmdtestp", "LIST", "files trimmed" )
        assertiCmd(s.adminsession,"irm -f --empty "+bunfile )
        assertiCmd(s.adminsession,"ils "+bunfile, "LIST", bunfile )
        assertiCmd(s.adminsession,"irm -rvf "+irodshome+"/icmdtestp", "LIST", "num files done" )
        assertiCmd(s.adminsession,"irm -f --empty "+bunfile )
        if os.path.exists(dir_w+"/testp"):
            shutil.rmtree( dir_w+"/testp" )
        shutil.rmtree( mysdir )
    
        os.unlink( sfile2 )
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
        if os.path.exists( mysdir ):
            shutil.rmtree( mysdir )
    
    
    
    
    
    
    
    
    
    
    
    
        irodshome = "/"+irodszone+"/home/rods/"+s.adminsession.sessionId
        sfile2 = dir_w+"/sfile2"
        commands.getstatusoutput( "cat "+progname+" "+progname+" > "+sfile2 )
        myldir = dir_w+"/ldir"
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
        assertiCmd(s.adminsession,"imkdir icmdtest")
    
        assertiCmd(s.adminsession,"irsync "+progname+" i:"+irodshome+"/icmdtest/foo100" )
        assertiCmd(s.adminsession,"irsync i:"+irodshome+"/icmdtest/foo100 "+dir_w+"/foo100" )
        assertiCmd(s.adminsession,"irsync i:"+irodshome+"/icmdtest/foo100 i:"+irodshome+"/icmdtest/foo200" )
        assertiCmd(s.adminsession,"irm -f "+irodshome+"/icmdtest/foo100 "+irodshome+"/icmdtest/foo200")
        assertiCmd(s.adminsession,"iput -R "+self.testresc+" "+progname+" "+irodshome+"/icmdtest/foo100")
        assertiCmd(s.adminsession,"irsync "+progname+" i:"+irodshome+"/icmdtest/foo100" )
        assertiCmd(s.adminsession,"iput -R "+self.testresc+" "+progname+" "+irodshome+"/icmdtest/foo200")
        assertiCmd(s.adminsession,"irsync i:"+irodshome+"/icmdtest/foo100 i:"+irodshome+"/icmdtest/foo200" )
        os.unlink( dir_w+"/foo100" )
    
        os.unlink( sfile2 )
    
    
    
    
    
    
    
    
    
    
        irodshome = "/"+irodszone+"/home/rods/"+s.adminsession.sessionId
        sfile2 = dir_w+"/sfile2"
        commands.getstatusoutput( "cat "+progname+" "+progname+" > "+sfile2 )
        myldir = dir_w+"/ldir"
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
        assertiCmd(s.adminsession,"imkdir icmdtest")
    
        lrsfile = dir_w+"/lrsfile"
        rsfile = dir_w+"/rsfile"
    
    
        assertiCmd(s.adminsession,"ilsresc", "LIST", self.testresc )
        assertiCmd(s.adminsession,"imiscsvrinfo", "LIST", "relVersion" )
        assertiCmd(s.adminsession,"iuserinfo", "LIST", "name: "+username )
        assertiCmd(s.adminsession,"ienv", "LIST", "Release Version" )
        assertiCmd(s.adminsession,"icd "+irodshome )
        assertiCmd(s.adminsession,"ipwd", "LIST", "home" )
        assertiCmd(s.adminsession,"ihelp ils", "LIST", "ils" )
        assertiCmd(s.adminsession,"ierror -14000", "LIST", "SYS_API_INPUT_ERR" )
        assertiCmd(s.adminsession,"iexecmd hello", "LIST", "Hello world" )
        assertiCmd(s.adminsession,"ips -v", "LIST", "ips" )
        assertiCmd(s.adminsession,"iqstat", "LIST", "No delayed rules" )
        assertiCmd(s.adminsession,"imkdir "+irodshome+"/icmdtest1" )
        assertiCmd(s.adminsession,"iput -kf  "+progname+"  "+irodshome+"/icmdtest1/foo1" )
        assertiCmd(s.adminsession,"ils -l "+irodshome+"/icmdtest1/foo1", "LIST", ["foo1", myssize] )
        assertiCmd(s.adminsession,"iadmin ls "+irodshome+"/icmdtest1", "LIST", "foo1" )
        assertiCmd(s.adminsession,"ichmod read "+s.sessions[1].getUserName()+" "+irodshome+"/icmdtest1/foo1" )
        assertiCmd(s.adminsession,"ils -A "+irodshome+"/icmdtest1/foo1", "LIST", s.sessions[1].getUserName()+"#"+irodszone+":read" )
        assertiCmd(s.adminsession,"irepl -B -R "+self.testresc+" "+irodshome+"/icmdtest1/foo1" )
        assertiCmd(s.adminsession,"itrim -S  "+irodsdefresource+" -N1 "+irodshome+"/icmdtest1/foo1" )
        assertiCmd(s.adminsession,"iphymv -R  "+irodsdefresource+" "+irodshome+"/icmdtest1/foo1" )
        assertiCmd(s.adminsession,"imeta add -d "+irodshome+"/icmdtest1/foo1 testmeta1 180 cm" )
        assertiCmd(s.adminsession,"imeta ls -d "+irodshome+"/icmdtest1/foo1", "LIST", "testmeta1" )
        assertiCmd(s.adminsession,"imeta ls -d "+irodshome+"/icmdtest1/foo1", "LIST", "180" )
        assertiCmd(s.adminsession,"imeta ls -d "+irodshome+"/icmdtest1/foo1", "LIST", "cm" )
        assertiCmd(s.adminsession,"icp -K -R "+self.testresc+" "+irodshome+"/icmdtest1/foo1 "+irodshome+"/icmdtest1/foo2" )
        assertiCmd(s.adminsession,"imv "+irodshome+"/icmdtest1/foo2 "+irodshome+"/icmdtest1/foo4" )
        assertiCmd(s.adminsession,"imv "+irodshome+"/icmdtest1/foo4 "+irodshome+"/icmdtest1/foo2" )
        assertiCmd(s.adminsession,"ichksum -K "+irodshome+"/icmdtest1/foo2", "LIST", "foo2" )
        assertiCmd(s.adminsession,"iget -f -K "+irodshome+"/icmdtest1/foo2 "+dir_w )
        os.unlink ( dir_w+"/foo2" )
        assertiCmd(s.adminsession,"irsync "+progname+" i:"+irodshome+"/icmdtest1/foo1" )
        assertiCmd(s.adminsession,"irsync i:"+irodshome+"/icmdtest1/foo1 /tmp/foo1" )
        assertiCmd(s.adminsession,"irsync i:"+irodshome+"/icmdtest1/foo1 i:"+irodshome+"/icmdtest1/foo2" )
        os.unlink ( "/tmp/foo1" )
    
    
        os.unlink( sfile2 )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        irodshome = "/"+irodszone+"/home/rods/"+s.adminsession.sessionId
        sfile2 = dir_w+"/sfile2"
        commands.getstatusoutput( "cat "+progname+" "+progname+" > "+sfile2 )
        myldir = dir_w+"/ldir"
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
        assertiCmd(s.adminsession,"imkdir icmdtest")
    
    
        lfile = dir_w+"/lfile"
        lfile1 = dir_w+"/lfile1"
        commands.getstatusoutput( "echo 012345678901234567890123456789012345678901234567890123456789012 > "+lfile )
            commands.getstatusoutput( "cat "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" > "+lfile1 )
            os.rename ( lfile1, lfile )
        os.mkdir( myldir )
        for i in range(1,3):
            mylfile = myldir+"/lfile"+str(i)
            mysfile = myldir+"/sfile"+str(i)
                shutil.copyfile( lfile, mylfile )
                os.rename( lfile, mylfile )
            shutil.copyfile( progname, mysfile )
    
        lrsfile = dir_w+"/lrsfile"
        rsfile = dir_w+"/rsfile"
        if os.path.isfile( lrsfile ):
            os.unlink( lrsfile )
        if os.path.isfile( rsfile ):
            os.unlink( rsfile )
        assertiCmd(s.adminsession,"iput -vbPKr --retries 10 --wlock -X "+rsfile+" --lfrestart "+lrsfile+" -N 2 "+myldir+" "+irodshome+"/icmdtest/testy", "LIST", "New restartFile" )
        assertiCmd(s.adminsession,"ichksum -rK "+irodshome+"/icmdtest/testy", "LIST", "Total checksum performed" )
        if os.path.isfile( lrsfile ):
            os.unlink( lrsfile )
        if os.path.isfile( rsfile ):
            os.unlink( rsfile )
        assertiCmd(s.adminsession,"irepl -BvrPT -R "+self.testresc+" --rlock "+irodshome+"/icmdtest/testy", "LIST", "icmdtest/testy" )
        assertiCmd(s.adminsession,"itrim -vrS "+irodsdefresource+" --dryrun --age 1 -N 1 "+irodshome+"/icmdtest/testy", "LIST", "This is a DRYRUN" )
        assertiCmd(s.adminsession,"itrim -vrS "+irodsdefresource+" -N 1 "+irodshome+"/icmdtest/testy", "LIST", "a copy trimmed" )
        assertiCmd(s.adminsession,"icp -vKPTr -N 2 "+irodshome+"/icmdtest/testy "+irodshome+"/icmdtest/testz", "LIST", "Processing lfile1" )
        assertiCmd(s.adminsession,"irsync -r i:"+irodshome+"/icmdtest/testy i:"+irodshome+"/icmdtest/testz" )
        assertiCmd(s.adminsession,"irm -vrf "+irodshome+"/icmdtest/testy" )
        assertiCmd(s.adminsession,"iphymv -vrS "+irodsdefresource+" -R "+self.testresc+" "+irodshome+"/icmdtest/testz", "LIST", "icmdtest/testz" )
    
        if os.path.isfile( lrsfile ):
            os.unlink( lrsfile )
        if os.path.isfile( rsfile ):
            os.unlink( rsfile )
        if os.path.exists(dir_w+"/testz"):
            shutil.rmtree( dir_w+"/testz" )
        assertiCmd(s.adminsession,"iget -vPKr --retries 10 -X "+rsfile+" --lfrestart "+lrsfile+" --rlock -N 2 "+irodshome+"/icmdtest/testz "+dir_w+"/testz", "LIST", "testz" )
        assertiCmd(s.adminsession,"irsync -r "+dir_w+"/testz i:"+irodshome+"/icmdtest/testz" )
        assertiCmd(s.adminsession,"irsync -r i:"+irodshome+"/icmdtest/testz "+dir_w+"/testz" )
        if os.path.isfile( lrsfile ):
            os.unlink( lrsfile )
        if os.path.isfile( rsfile ):
            os.unlink( rsfile )
        output = commands.getstatusoutput( "diff -r "+dir_w+"/testz "+myldir )
        print "output is ["+str(output)+"]"
        assertiCmd(s.adminsession,"iput -N0 -R "+self.testresc+" "+myldir+"/lfile1 "+irodshome+"/icmdtest/testz/lfoo100" )
        if os.path.isfile( dir_w+"/lfoo100" ):
            os.unlink( dir_w+"/lfoo100" )
        assertiCmd(s.adminsession,"iget -N0 "+irodshome+"/icmdtest/testz/lfoo100 "+dir_w+"/lfoo100" )
        output = commands.getstatusoutput( "diff "+myldir+"/lfile1 "+dir_w+"/lfoo100" )
        print "output is ["+str(output)+"]"
        shutil.rmtree( dir_w+"/testz" )
        os.unlink( dir_w+"/lfoo100" )
        assertiCmd(s.adminsession,"irm -vrf "+irodshome+"/icmdtest/testz" )
    
        os.unlink( sfile2 )
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
    
    
    
    
    
    
    
    
    
    
        irodshome = "/"+irodszone+"/home/rods/"+s.adminsession.sessionId
        sfile2 = dir_w+"/sfile2"
        commands.getstatusoutput( "cat "+progname+" "+progname+" > "+sfile2 )
        myldir = dir_w+"/ldir"
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )
        assertiCmd(s.adminsession,"imkdir icmdtest")
    
    
        lfile = dir_w+"/lfile"
        lfile1 = dir_w+"/lfile1"
        commands.getstatusoutput( "echo 012345678901234567890123456789012345678901234567890123456789012 > "+lfile )
            commands.getstatusoutput( "cat "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" "+lfile+" > "+lfile1 )
            os.rename ( lfile1, lfile )
        os.mkdir( myldir )
        for i in range(1,3):
            mylfile = myldir+"/lfile"+str(i)
            mysfile = myldir+"/sfile"+str(i)
                shutil.copyfile( lfile, mylfile )
                os.rename( lfile, mylfile )
            shutil.copyfile( progname, mysfile )
    
        lrsfile = dir_w+"/lrsfile"
        rsfile = dir_w+"/rsfile"
        if os.path.isfile( lrsfile ):
            os.unlink( lrsfile )
        if os.path.isfile( rsfile ):
            os.unlink( rsfile )
        assertiCmd(s.adminsession,"iput -vQPKr --retries 10 -X "+rsfile+" --lfrestart "+lrsfile+" "+myldir+" "+irodshome+"/icmdtest/testy", "LIST", "icmdtest/testy" )
        assertiCmd(s.adminsession,"irepl -BQvrPT -R "+self.testresc+" "+irodshome+"/icmdtest/testy", "LIST", "icmdtest/testy" )
        assertiCmd(s.adminsession,"itrim -vrS "+irodsdefresource+" -N 1 "+irodshome+"/icmdtest/testy", "LIST", "a copy trimmed" )
        assertiCmd(s.adminsession,"icp -vQKPTr "+irodshome+"/icmdtest/testy "+irodshome+"/icmdtest/testz", "LIST", "Processing sfile1" )
        assertiCmd(s.adminsession,"irm -vrf "+irodshome+"/icmdtest/testy" )
        if os.path.isfile( lrsfile ):
            os.unlink( lrsfile )
        if os.path.isfile( rsfile ):
            os.unlink( rsfile )
        if os.path.exists(dir_w+"/testz"):
            shutil.rmtree( dir_w+"/testz" )
        assertiCmd(s.adminsession,"iget -vQPKr --retries 10 -X "+rsfile+" --lfrestart "+lrsfile+" "+irodshome+"/icmdtest/testz "+dir_w+"/testz", "LIST", "Processing sfile2" )
        if os.path.isfile( lrsfile ):
            os.unlink( lrsfile )
        if os.path.isfile( rsfile ):
            os.unlink( rsfile )
        output = commands.getstatusoutput( "diff -r "+dir_w+"/testz "+myldir )
        print "output is ["+str(output)+"]"
        shutil.rmtree( dir_w+"/testz" )
        assertiCmd(s.adminsession,"irm -vrf "+irodshome+"/icmdtest/testz" )
        shutil.rmtree( myldir )
    
    
        os.unlink( sfile2 )
        if os.path.exists( myldir ):
            shutil.rmtree( myldir )