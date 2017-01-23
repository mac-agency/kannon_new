#!/usr/bin/perl

#------------------------------------------------------------------------------
# 以下はサーバー仕様に理解がある方のみ、必要に応じて変更が可能です。
#------------------------------------------------------------------------------

# 【データフォルダの名称及び設置パスを設定】
# データファイルの保存する場所を、絶対パスもしくは相対パスで指定してください。
$install_datadir = './rakumail_data';

# 【画像フォルダの名称及び設置パスを設定】
# 画像ファイルの保存する場所を、絶対パスもしくは相対パスで指定してください。
$install_imgdir = './rakumail_img';

# 【非suEXEC時のサブフォルダ名称を設定】
# suEXEC環境でない場合に必要な、サブフォルダの名称を指定してください。
# （※パスの変更は出来ません）
$Exception_dir_name = 'cgi';

#【購入URL】
# 製品購入用のURLを指定してください。
$product_url = 'http://www.raku-mail.com/';

#------------------------------------------------------------------------------
# 以下は変更しないでください。
#------------------------------------------------------------------------------
&method_ck();

$uid = &suExec( $self );
$self = 'rm_install.cgi';
$serial = '43544d2d4c4943454e5345';
$setup = 'rakumail.cgi';
$product_name = '楽メールEX';
$product_edition = '体験版';
$system_code = 'rakumailex';
$system_sign = 'C';
$script_cgi = 'acc.cgi';
$data_dir = 'rakumail_data';
$img_dir = 'rakumail_img';
$ex_dir = 'cgi';
$product = $product_name. ' ['. $product_edition.']';
$install_base_dir = './';
$style_default = 'display:none;';
$Exception_dir_path = $Exception_dir_name;
$Exception_dir_path = &dirClean($Exception_dir_path);
$Exception_dir_path .= '/';
$self = &get_self( $self);
$uid = &suExec( $self );

my( $install_datadir_base, $install_datadir_name ) = &chkInstalldir($install_datadir);
my( $install_imgdir_base, $install_imgdir_name ) = &chkInstalldir($install_imgdir);

$Exception_flag = 0;
if( defined $param{'ex'} && $param{'ex'} > 0 ){
	$Exception_flag = 1;
	if( $install_datadir_base eq './' ){
		$install_datadir_base = './'.$Exception_dir_path;
	}
	if( $install_imgdir_base eq './' ){
		$install_imgdir_base = './'.$Exception_dir_path;
	}
	$setup = $Exception_dir_path.$setup;
	$script_cgi = $Exception_dir_path. $script_cgi;
	$install_base_dir .= $Exception_dir_path;
}

# インストール環境確認
my $install_datadir_path = $install_datadir_base;
$install_datadir_path .= $install_datadir_name if( $install_datadir_name ne "" );
my $install_imgdir_path = $install_imgdir_base;
$install_imgdir_path .= $install_imgdir_name if( $install_imgdir_name ne "" );
$default_data_dir = $data_dir;
$default_img_dir = $img_dir;
# 表示スタイル決定
$check_install_datadir = $install_datadir_path;
$check_install_imgdir = $install_imgdir_path;
$check_install_datadir =~ s/\/$//;
$check_install_imgdir =~ s/\/$//;
$style_install_data_default =$style_default;
$style_install_data_change = $style_default;
$style_install_img_default = $style_default;
$style_install_img_change = $style_default;
if( $Exception_flag ){
	$default_data_dir = $ex_dir. '/'.$default_data_dir;
	$default_img_dir = $ex_dir. '/'.$default_img_dir;
	$style_install_data_default = ( $check_install_datadir eq './'.$ex_dir.'/'.$data_dir )? '': $style_default;
	$style_install_data_change = ( $check_install_datadir ne './'.$ex_dir.'/'.$data_dir )? '': $style_default;
	$style_install_img_default = ( $check_install_imgdir eq './'.$ex_dir.'/'.$img_dir )? '': $style_default;
	$style_install_img_change = ( $check_install_imgdir ne './'.$ex_dir.'/'.$img_dir )? '': $style_default;
}else{
	$style_install_data_default = ( $check_install_datadir eq './'.$data_dir )? '': $style_default;
	$style_install_data_change = ( $check_install_datadir ne './'.$data_dir )? '': $style_default;
	$style_install_img_default = ( $check_install_imgdir eq './'.$img_dir )? '': $style_default;
	$style_install_img_change = ( $check_install_imgdir ne './'.$img_dir )? '': $style_default;
}


use Socket;

if( -w $install_base_dir && -w $install_datadir_base && -w $install_imgdir_base && !&chkDirformat($install_datadir) && !&chkDirformat($install_imgdir) && !&chkDirName($Exception_flag,$Exception_dir_name) ){
	
	if( $param{'mode'} eq 'start' ){
		&header_nocache();
		print "Content-type: text/plain","\n\n";
		my %query = (
			'get' => 'list',
			'serial' => $serial,
			'pc' => $system_code
		);
		my @list = &get_resource( \%err, {%query}, 'list' );
		if( $err{'error'} ne "" ){
			my $error_kind = $err{'error'} eq 'status' ? 'socket_04': 'socket_'.$err{'error'};
			print '{"error":1,"err_kind":"'. $error_kind .'"}';
			exit;
		}
		if( ! @list ){
			print '{"error":1,"err_kind":"license"}';
			exit;
		}
		my @json_array = ();
		foreach my $line ( @list ){
			$line =~ s/\s+$//g;
			my @lines = split(/\t/,$line);
			my $filename = ( split(/\//,$lines[1]) )[-1];
			$lines[4] = $filename;
			my $block = '["'.join('","',@lines). '"]';
			push @json_array, $block;
		}
		print '{"list":[';
		print join(",",@json_array);
		print ']}';
		exit;
	}
	
	if( $param{'mode'} eq 'source' ){
		my $start_time = time();
		my $path = $param{'path'};
		my $opt = $param{'opt'};
		my %query = (
			'get' => 'source',
			'serial' => $serial,
			'package' => $param{'package'},
			'path' => $path,
			'opt' => $param{'opt'},
			'pc' => $system_code
		);
		my $data = &get_resource( \%err, {%query} );
		my @filepath = split(/\//,$path);
		my $filename = $filepath[-1];
		
		# 起動スクリプト以外
		if( index( $path, $data_dir ) == 0 ){
			shift @filepath;
			unshift @filepath, $install_datadir_path;
			$path = join("/",@filepath);
		}elsif( index( $path, $img_dir ) == 0 ){
			shift @filepath;
			unshift @filepath, $install_imgdir_path;
			$path = join("/",@filepath);
		}else{
			if( $Exception_flag > 0 ){
				$path = $Exception_dir_path. $path;
			}
		}
		
		&header_nocache();
		print "Content-type: text/plain", "\n\n";
		
		# タイムアウト
		my $utime = $param{'utime'};
		if( time() - $start_time >= 9 ){
			print '{"error":1,"err_kind":"timeout"}';
			exit;
		}
		
		if( $err{'error'} ne "" ){
			my $error_kind = $err{'error'} eq 'status' ? 'socket_04': 'socket_'.$err{'error'};
			print '{"error":1,"err_kind":"'. $error_kind .'"}';
			exit;
		}
		
		if( $opt eq 'dir' ){
			if( -d $path ){
				if( ! -w $path ){
					print '{"error":1,"err_kind":"dircheck"}';
					exit;
				}
			}else{
				mkdir( $path, 0707 );
			}
			if( $uid ){
				if( ! chown( $uid, -1, $path ) ){
					rmdir $path;
					print '{"error":1,"err_kind":"chown"}';
					exit;
				}
				if( &chkChown( $self, $path ) ){
					rmdir $path;
					print '{"error":1,"err_kind":"chown"}';
					exit;
				}
			}
			
			chmod 0707, $path;
			print '{"error":0}';
			exit;
		}
		if( $filename !~ /index\.htm/ &&  ! $data ){
			print '{"error":1,"err_kind":"download"}';
			exit;
		}
		if( ! open( FILE, ">$path" ) ){
			print '{"error":1,"err_kind":"overwrite"}';
			exit;
		}
		binmode(FILE);
		my $pms = '0606';
		if( $opt eq 'cgi' ){
			my $perlpath = &getPerlpath();
			$data =~ s|^[^\s]+|$perlpath|m;
			$pms = '0705';
			if( $Exception_flag ){
				$filename = $Exception_dir_path. $filename;
				
			}
			if( $setup eq $filename ){
				my $base_path = $install_datadir_path;
				my $base_img_path = $install_imgdir_path;
				
				if( $Exception_flag ){
					$Exception_dir = $Exception_dir_path;
					if( $Exception_dir !~ /^\./ ){
						$Exception_dir = './'.$Exception_dir;
					}
					if( $base_path !~ /^\// ){
						if( $base_path !~ /^\./ ){
							$base_path = './'. $base_path;
						}
						if( $base_path !~ /\/$/ ){
							$base_path .= '/';
						}
						if( $base_path =~ /^\Q$Exception_dir\E/ ){
							$base_path =~ s/^\Q$Exception_dir\E/\.\//;
						}else{
							if( $base_path =~ /^\.\.\// ){
								$base_path = '../'. $base_path;
							}else{
								$base_path = '.'. $base_path;
							}
						}
					}
					if( $base_img_path !~ /^\// ){
						if( $base_img_path !~ /^\./ ){
							$base_img_path = './'. $base_img_path;
						}
						if( $base_img_path !~ /\/$/ ){
							$base_img_path .= '/';
						}
						if( $base_img_path =~ /^\Q$Exception_dir\E/ ){
							$base_img_path =~ s/^\Q$Exception_dir\E/\.\//;
						}else{
							if( $base_img_path =~ /^\.\.\// ){
								$base_img_path = '../'. $base_img_path;
							}else{
								$base_img_path = '.'. $base_img_path;
							}
						}
						
					}
				}else{
					$base_path .= '/';
					$base_img_path .= '/';
				}
				$data =~ s|\$BASE_DIR([^;]+?);|\$BASE_DIR = '$base_path';|m;
				$data =~ s|\$DEF_IMGDIR([^;]+?);|\$DEF_IMGDIR = '$base_img_path';|m;
			}
		}
		print FILE $data;
		if( $uid ){
			if( ! chown( $uid, -1, $path ) ){
				unlink $path;
				print '{"error":1,"err_kind":"chown"}';
				exit;
			}
			if( &chkChown( $self, $path ) ){
				unlink $path;
				print '{"error":1,"err_kind":"chown"}';
				exit;
			}
		}
		
		chmod oct($pms), $path;
		
		# 購入用URL挿入
		if( $filename eq 'ini_atv_pl.cgi' && $product_url ne "" ){
			my @aff_path_array = split(/\//,$path);
			$aff_path_array[-1] = 'ini_aff_pl.cgi';
			$aff_path = join( "/", @aff_path_array );
			open( AFF, ">$aff_path" );
			print AFF $product_url;
			close(AFF);
			chmod oct($pms), $aff_path;
			if( $uid ){
				chown( $uid, -1, $aff_path );
			}
		}
		
		print '{"error":0}';
		exit;
	}
	if( $param{'mode'} eq 'finish' ){
		$error = 0;
		$d_self_error = 0;
		$ex_error = 0;
		if( $Exception_flag ){
			if( &getPms( $Exception_dir_path ) ne '705' ){
				$ex_error = chmod( 0705, $Exception_dir_path ) ? 0: 1;
				$error = 1 if( $ex_error );
			}
			if( !$error ){
				my $flag = unlink $self || 0;
				$error = 1 if( !$flag );
				$d_self_error = $flag ? 0: 1;
			}
		}else{
			my $flag = unlink $self || 0;
			$error = 1 if( !$flag );
			$d_self_error = $flag ? 0: 1;
		}
		
		&header_nocache();
		print "Content-type: text/plain","\n\n";
		print '{"error":'.$error.',"self_error":'.$d_self_error.',"ex_error":'.$ex_error.'}';
		exit;
	}
	if( $param{'mode'} eq 'defined' ){
		print "Content-type: text/plain","\n\n";
		print '{"ok":1}';
		exit;
	}
}

#-------------------------------------------
# HTML出力
#-------------------------------------------
&header_nocache();
print "Content-type: text/html; charset=utf-8", "\n\n";
print <<"END";
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE8">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<meta http-equiv="Content-Script-Type" content="text/javascript" />
<meta name="robots" content="noindex,nofollow" />
<title>$product_name - インストーラー -</title>
<link href="https://www.atmarkweb.jp/install/oem_custom/rakumailex/images/style.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="https://www.atmarkweb.jp/install/js/jquery/jquery-1.7.1.min.js"></script>
<script type="text/javascript">

END

print <<'END';
if( !atweb ) var atweb={};
if( !atweb.installer ) atweb.installer={};
atweb.installer.flag = {};
atweb.installer.timeover = {};
atweb.installer.exception = 0;
atweb.installer.process = 0;

$(document).ready(function(){
	document.URL.split("/");
	var urls = document.URL.split('#')[0].split('?')[0].split('/');
	urls.pop();
	var url = urls.join('/');
	$("#current_url1").html(url);
	$("#current_url2").html(url);
	$("#current_url3").html(url);
	$("#current_url4").html(url);
});

// 開始
atweb.installer.start = function(ex){
	
	if( ex && ex > 0 )
		atweb.installer.exception = 1;
	
	$("div#install_start").hide();
	$("div#download_process_load").show();
	$("div#install_progress").show();
	
	callback = function(json){
		
		if( atweb.installer.flag.timeover > 0 ){
			return;
		}
		atweb.installer.flag.timeover = 1;
		atweb.installer.socketerror = function(){
			if( atweb.installer.flag.list > 0 ){
				return;
			}
			atweb.installer.timeover.list = 1;
			atweb.installer.error('socket_03');
			return;
		}	
		$.getJSON( '?mode=start', function(json){
			if( atweb.installer.timeover.list > 0 ){
				return;
			}
			atweb.installer.flag.list = 1;
			if( json['error'] && json['error'] > 0 ){
				atweb.installer.error(json['err_kind']);
				return;
			}
			
			atweb.installer.list =  json['list'];
			var len = 0;
			jQuery.each( json['list'], function(i){
				if( json['list'][i][3] != 'dir' ){
					len++;
				}
			});
			
			$("span#count").html(0);
			$("span#total").html(len);
			
			atweb.installer.len = atweb.installer.list.length;
			atweb.installer.count = 0;
			atweb.installer.counter = 0;
			atweb.installer.download();
		});
		setTimeout( atweb.installer.socketerror, 10000 );
	}
	
	$.getJSON("http://www.atmarkweb.jp/install/json/p.cgi?callback=?");
	
	atweb.installer.timeout = function(){
		if( atweb.installer.flag.timeover > 0 ){
			return;
		}
		atweb.installer.flag.timeover = 1;
		atweb.installer.error('timeout');
		return;
	}
	setTimeout( atweb.installer.timeout, 10000 );
}

// ダウンロード
atweb.installer.download = function(){
	
	if( atweb.installer.count >= atweb.installer.len ){
		var url = '?mode=finish';
		if( atweb.installer.exception > 0 )
			url += '&ex=1';
		
		// 完了処理
		$.getJSON( url, function(json){
			
			atweb.installer.flag.finish = 1;
			$("#finish_setup").hide();
			$("#finish_ok").hide();
			$("#finish_bad").hide();
			$("#finish_ex_bad").hide();
			$("#gotoSetup").hide();
			$("#reconfirmSetup").hide();
			$("#delconfirmSetup").hide();
			if( json['error'] > 0 ){
				if( json['self_error'] == 1 ){
					$("#finish_bad").show();
					$("#delconfirmSetup").show();
				}
				if( json['ex_error'] == 1 ){
					$("#finish_ex_bad").show();
					$("#reconfirmSetup").show();
				}
			}else{
				$("#gotoSetup").show();
				$("#finish_setup").show();
				$("#finish_ok").show();
			}
			
			$("#progress_filename").html('--');
			$("div#download_process_load").hide();
			$("div#download_process_finish").show();
			$("#install_finish").show();
		});
		
		atweb.installer.timeout = function(){
			if( atweb.installer.flag.finish > 0 ){
				return;
			}
			$("#finish_ok").hide();
			$("#finish_bad").show();
			$("#progress_filename").html('--');
			$("div#download_process_load").hide();
			$("div#download_process_finish").show();
			$("#install_finish").show();
			return;
		}
		setTimeout( atweb.installer.timeout, 2000 );
		return;
	}
	
	// ダウンロード実行
	var count = atweb.installer.count;
	var obj = atweb.installer.list[count];
	var utime = Math.round(new Date().getTime() / 1000);
	var url = '?mode=source&package=' + obj[0] + '&path='+ obj[1] + '&pms=' + obj[2] + '&opt=' + obj[3];
	url += '&utime='+ utime;
	atweb.installer.process++;
	var _process = atweb.installer.process;
	
	/* 例外 */
	if( atweb.installer.exception > 0 )
		url += '&ex=1';
	$("#progress_filename").html(obj[4]);
	
	$.getJSON( url, function(json){
		// 強制タイムアウト
		if( json['error'] && json['error'] > 0 ){
			if( json['err_kind'] == 'timeout' ){
				return;
			}
		}
		if( atweb.installer.flag[_process] > 0 ){
			return;
		}
		atweb.installer.flag[_process] = 1;
		
		if( json['error'] && json['error'] > 0 ){
			atweb.installer.error(json['err_kind']);
			return;
		}
		
		// １つ進める
		atweb.installer.count++;
		
		if( obj[3] == 'dir' ){
			atweb.installer.download();
		}else{
			atweb.installer.counter++;
			$("span#count").html(atweb.installer.counter);
			setTimeout(atweb.installer.download , 50);
		}
	});
	
	atweb.installer.timeout = function(t){
		if( !t && atweb.installer.flag[_process] > 0 ){
			return;
		}
		atweb.installer.flag[_process] = 1;
		
		$("#restart").hide();
		$("#restart_ex").hide();
		$("#restart_download").show();
		
		atweb.installer.error('timeout');
	}
	setTimeout( atweb.installer.timeout, 10000 );
}

atweb.installer.download_restart = function(){
	
	$("#restart").hide();
	$("#restart_ex").hide();
	$("#restart_download").hide();
	if( atweb.installer.exception > 0 ){
		$("#restart_ex").show();
	}else{
		$("#restart").show();
	}
	
	$("#download_process_load").show();
	$("#download_process_error").hide();
	$("#download_process_finish").hide();
	$("#install_error").hide();
	
	$("#install_error div[id^=error]").each(function(){
		$(this).hide();
	});
	
	atweb.installer.download();
}

atweb.installer.reconfirm = function(){
	$("#install_finish").hide();
	setTimeout( atweb.installer.download, 500 );
}

atweb.installer.delcofirm = function(url){
	$("#install_finish").hide();
	
	__func = function(){
		var data = { "mode" : "defined" };
		$.ajax({
			type: "POST",
			url: url,
			data: data,
			success: function(data, dataType){
				$("#install_finish").show();
			},
			error: function(){
				$("#finish_bad").hide();
				$("#delconfirmSetup").hide();
				$("#gotoSetup").show();
				$("#finish_setup").show();
				$("#install_finish").show();
			}
		});
	}
	setTimeout( __func, 500 );
}

// エラー表示
atweb.installer.error = function(k){
	if( k == 'socket_02' ){
		$("#error_serverhost").show();
	}
	if( k == 'socket_03' ){
		$("#error_socket").show();
	}
	if( k == 'socket_04' ){
		$("#error_serverconect").show();
	}
	if( k == 'timeout' ){
		$("#error_servertimeout").show();
	}
	if( k == 'license' ){
		$("#error_license").show();
	}
	if( k == 'dircheck' ){
		$("#error_dircheck").show();
	}
	if( k == 'overwrite' ){
		$("#error_overwrite").show();
	}
	if( k == 'download' ){
		$("#error_download").show();
	}
	if( k == 'chown' ){
		$("#error_chown").show();
	}
	$("div#download_process_load").hide();
	$("div#download_process_finish").hide();
	$("#download_process_error").show();
	$("#install_error").show();
	
}
END

print <<"END";
</script>
</head>
<body id="install">
<div id="layout">
  <div id="layout_body"> 
    <!-- header -->
    <div id="layout_body_header" style="background: url('https://www.atmarkweb.jp/install/oem_custom/rakumailex/images/rakumaillogo.jpg') no-repeat 0px;"> <br class="clear_both" />
    </div>
    <!-- //header --> 
    <!-- main -->
    <div id="layout_body_main">
      <div id="main_header">
        <dl id="main_header_title">
          <dt>$product_name インストーラー</dt>
        </dl>
        <p id="main_header_comment">ソフトウェアのインストールをおこないます。</p>
      </div>
      <br />
      <br />
      <blockquote>
        <div id="install_ready" style="$style_default">
          <table class="tb_cover">
            <tr>
              <td><div class="dialog01">
                  <div class="header">
                    <div class="c"></div>
                  </div>
                  <div class="body">
                    <div class="c">
                      <div class="dialog_data">
                        <table class="tb_config">
                          <tr>
                            <th>▼製品情報</th>
                          </tr>
                          <tr>
                            <td>以下の製品をインストールします。<br />
                              <div style="margin-top:10px;">【製品名】<br />
                                <span style="margin-left:10px;">$product_name</span></div></td>
                          </tr>
                        </table>
                        <br>
                        <table class="tb_config">
                          <tr>
                            <th>▼インストール場所</th>
                          </tr>
                          <tr>
                            <td> 以下の場所にインストールを実行します。<br />
                              <div style="margin-top:10px;">【メインプログラムのURL】<br />
                                <span id="current_url1" style="color:#6C6; margin-left:10px;">http://</span>/<span>$setup</span></div>
                              <div style="margin-top:10px;">【サブプログラムのURL】<br />
                                <span id="current_url2" style="color:#6C6; margin-left:10px;">http://</span>/<span>$script_cgi</span></div>
                              <div style="margin-top:10px; $style_install_img_default">【画像フォルダ<span style="margin-top:10px;">のURL</span>】<br />
                                <span id="current_url3" style="color:#6C6; margin-left:10px;">http://</span>/<span>$default_img_dir/</span></div>
                              <div style="margin-top:10px; $style_install_data_default">【データフォルダ<span style="margin-top:10px;">のURL</span>】<br />
                                <span id="current_url4" style="color:#6C6; margin-left:10px;">http://</span>/<span>$default_data_dir/</span></div>
                              <div style="margin-top:10px; $style_install_img_change">【画像フォルダのパス】　<span style="color:#C66;">※初期位置より変更されています</span><br />
                                <span style="color:#C66; margin-left:10px;">$install_imgdir_base</span><span>$install_imgdir_name</span></div>
                              <div style="margin-top:10px; $style_install_data_change">【データフォルダのパス】　<span style="color:#C66;">※初期位置より変更されています</span><br />
                                <span style="color:#C66; margin-left:10px;">$install_datadir_base</span><span>$install_datadir_name</span></div>
                              <br />
                              <div class="alert1"><span>すでにファイルが存在する場合には、<br />
                                全て上書きされてしまいますのでご注意ください。</span></div></td>
                          </tr>
                        </table>
                      </div>
                    </div>
                  </div>
                  <div class="footer">
                    <div class="c"></div>
                  </div>
                </div></td>
            </tr>
          </table>
          <br />
          <br>
        </div>
        <div id="install_progress" style="$style_default">
          <table class="tb_cover">
            <tr>
              <td><div class="dialog01">
                  <div class="header">
                    <div class="c"></div>
                  </div>
                  <div class="body">
                    <div class="c">
                      <div class="dialog_data">
                        <table class="tb_config">
                          <tr>
                            <th colspan="2" class="th_color2">▼インストール状況</th>
                          </tr>
                          <tr>
                            <td class="td_title">ファイル数</td>
                            <td align="center"><span id="count">--</span> / <span id="total">--</span></td>
                          </tr>
                          <tr>
                            <td class="td_title">対象ファイル</td>
                            <td align="center"><div id="progress_filename">準備中</div></td>
                          </tr>
                          <tr>
                            <td class="td_title">状況</td>
                            <td valign="middle"><div id="download_process_load" style="$style_default"><img src="https://www.atmarkweb.jp/install/oem_custom/rakumailex/images/loading_s.gif" width="16" height="16" /><span style="padding-left:5px; padding-top:-5px;">ただいまインストール中です...</span>
                                <div class="help1"><span>このままブラウザを閉じずにお待ちください。</span></div>
                              </div>
                              <div id="download_process_error" style="$style_default">エラーが発生しました</div>
                              <div id="download_process_finish" style="$style_default">完了しました</div></td>
                          </tr>
                        </table>
                      </div>
                    </div>
                  </div>
                  <div class="footer">
                    <div class="c"></div>
                  </div>
                </div></td>
            </tr>
          </table>
          <br />
        </div>
        <div id="install_error" class="check_ng" style="$style_default">
          <table>
            <tr>
              <th>エラーが発生しました。</th>
            </tr>
            <tr>
              <td class="td_config"><div id="error_datadir" style="margin-top:10px;$style_default">【保存先エラー】<br>
                  データフォルダの保存先に、フォルダ名の記載がありません。<br>
                  フォルダ名を記述して再試行してください。 </div>
                <div id="error_imgdir" style="margin-top:10px;$style_default">【保存先エラー】<br>
                  画像フォルダの保存先に、フォルダ名の記載がありません。<br>
                  フォルダ名を記述して再試行してください。 </div>
                <div id="error_suexec" style="margin-top:10px;$style_default">【パーミッションエラー】<br>
                  インストールができませんでした。<br>
                  $self を設置したフォルダのパーミッション（属性）を[707 or 700]に変更後、再試行してください。 </div>
                <div id="error_nosuexec" style="margin-top:10px;$style_default">【環境エラー】<br>
                  このサーバーはsuEXEC環境ではありません。<br>
                  suEXECに対応していない場合、以下の追加作業が必要となります。
                  <ol style="color:#000;">
                    <li>FTPでログインし、$selfを設置した位置に「<span style="color:#C66;">$Exception_dir_name</span>」フォルダを新規作成してください。 </li>
                    <br>
                    <li>「<span style="color:#C66;">$Exception_dir_name</span>」フォルダのパーミッション（属性）を[<span style="color:#C66;">707</span>]に変更して、再試行ボタンを押してください。</li>
                  </ol>
                </div>
                <div id="error_nosuexec_ex" style="margin-top:10px;$style_default">【環境エラー】<br>
                  <br>
                  <strong>再試行の結果、動作しませんでした。<br>
                  追加作業に誤りがないか確認してください。<br>
                  </strong> <br>
                  このサーバーはsuEXEC環境ではありません。<br>
                  suEXECに対応していない場合、以下の追加作業が必要となります。
                  <ol style="color:#000;">
                    <li>FTPでログインし、$selfを設置した位置に「<span style="color:#C66;">$Exception_dir_name</span>」フォルダを新規作成してください。 </li>
                    <br>
                    <li>「<span style="color:#C66;">$Exception_dir_name</span>」フォルダのパーミッション（属性）を[<span style="color:#C66;">707</span>]に変更して、再試行ボタンを押してください。</li>
                  </ol>
                </div>
                <div id="error_datadir_non" style="margin-top:10px;$style_default">【フォルダチェックエラー】<br>
                  データフォルダの設定パスについて、指定した $install_datadir_base が見つかりません。 <br>
                  パスの記述に誤りがないか、指定パスのフォルダが存在するか確認してください。</div>
                <div id="error_imgdir_non" style="margin-top:10px;$style_default">【フォルダチェックエラー】<br>
                  画像フォルダの設定パスについて、指定した $install_imgdir_base が見つかりません。 <br>
                  パスの記述に誤りがないか、指定パスのフォルダが存在するか確認してください。</div>
                <div id="error_datadir_format" style="margin-top:10px;$style_default"> 【書式エラー】<br />
                  データフォルダの設定パスについて、設置パスの記述に書式上の誤りがあります。 </div>
                <div id="error_imgdir_format" style="margin-top:10px;$style_default"> 【書式エラー】<br />
                  画像フォルダの設定パスについて、設置パスの記述に書式上の誤りがあります。 </div>
                <div id="error_dirname_ex" style="margin-top:10px;$style_default"> 【書式エラー】<br />
                  サブフォルダ「<span style="color:#C66;">$Exception_dir_name</span>」について、パスの指定はできません。<br>
                  名称のみ記述してください。</div>
                <div id="error_dircheck" style="margin-top:10px;$style_default"> 【フォルダチェックエラー】<br>
                  インストール先フォルダが既に存在し、上書きできない状態になっています。 <br>
                  違う場所に設置するか、既存のフォルダをFTPで手動削除してください。<br />
                </div>
                <div id="error_overwrite" style="margin-top:10px;$style_default"> 【上書きエラー】<br />
                  インストール先ファイルが既に存在し、上書きできない状態になっています。 <br>
                  違う場所に設置するか、既存のファイルをFTPで手動削除してください。<br>
                </div>
                <div id="error_chown" style="margin-top:10px;$style_default"> 【環境エラー】<br />
                  作成したフォルダ・ファイルの所有権を変更できないため、正常にインストールできません。 <br>
                  サポートセンターにお問い合わせください。<br>
                </div>
                <div id="error_license" style="margin-top:10px;$style_default"> 【ライセンスエラー】<br />
                  ライセンス情報が不正です。<br>
                  インストールは停止しました。</div>
                <div id="error_serverhost" style="margin-top:10px;$style_default"> 【接続エラー】<br />
                  ホストが見つからないため、ダウンロードサーバーに接続できません。<br>
                  しばらく待ってから再試行してください。</div>
                <div id="error_socket" style="margin-top:10px;$style_default"> 【接続エラー】<br />
                  このサーバーではソケットが利用できないため、ファイルをダウンロードできません。<br>
                  インストールをおこなうには、サーバーがソケット通信に対応している必要があります。 </div>
                <div id="error_serverconect" style="margin-top:10px;$style_default">【接続エラー】<br />
                  ダウンロードサーバーに接続できません。<br>
                  しばらく待ってから再試行してください。</div>
                <div id="error_servertimeout" style="margin-top:10px;$style_default"> 【接続エラー】<br />
                  タイムアウトのため、ダウンロードサーバーに接続できません。<br>
                  しばらく待ってから再試行してください。</div>
                <div id="error_download" style="margin-top:10px;$style_default"> 【ダウンロードエラー】<br />
                  インストールファイルのダウンロードができません。 <br>
                  しばらく待ってから再試行してください。</div></td>
            </tr>
            <tr id="install_retry">
              <td class="td_color5">
                <input name="button" type="button" value="　再試行　" onClick="location.href='$self'" id="restart" />
                <input name="button" type="button" value="　再試行　" onClick="location.href='$self?ex=1'" id="restart_ex" />
                <input name="button" type="button" value="　再試行　" onClick="atweb.installer.download_restart();" id="restart_download" /></td>
            </tr>
          </table>
        </div>
        <br>
        <div id="install_start" style="$style_default">
          <table id="table_complete" class="tb_cover">
            <tr>
              <td><div class="dialog01">
                  <div class="header">
                    <div class="c"></div>
                  </div>
                  <div class="body">
                    <div class="c">
                      <div class="dialog_data">
                        <table class="tb_config">
                          <tr>
                            <th class="th_color2">▼インストールの開始</th>
                          </tr>
                          <tr>
                            <td>インストールを始めるには、<br />
                              「開始」ボタンを押して進んでください。</td>
                          </tr>
                          <tr>
                            <td class="td_color5"><input type="button" value="　開始　" onClick="atweb.installer.start();" id="downstart" />
                              <input type="button" value="　開始　" onClick="atweb.installer.start(1);" id="downstart_ex" /></td>
                          </tr>
                        </table>
                      </div>
                    </div>
                  </div>
                  <div class="footer">
                    <div class="c"></div>
                  </div>
                </div></td>
            </tr>
          </table>
          <br />
        </div>
        <div id="install_finish" style="$style_default">
          <table id="table_complete" class="tb_cover">
            <tr>
              <td><div class="dialog01">
                  <div class="header">
                    <div class="c"></div>
                  </div>
                  <div class="body">
                    <div class="c">
                      <div class="dialog_data">
                        <table class="tb_config">
                          <tr>
                            <th class="th_color2">▼インストールの完了</th>
                          </tr>
                          <tr>
                            <td><div id="finish_setup">インストールが完了しました。<br />
                              「セットアップ画面へ」ボタンを押して次の工程に進んでください。<br />
                              </div>
                              <div id="finish_bad" style="$style_default">
                                <div class="alert1"><span>【ファイルチェックエラー】<br>
                                  インストーラーファイル「$self」の削除が<br>
                                  自動処理できませんでした。</span></div>
                                <div style="margin:10px;">以下の作業をおこなってください。</div>
                                <ol>
                                  <li>FTPでログインし、<span style="color:#C66;">$self</span>を手動で削除してください。 </li>
                                  <br>
                                  <li>「再試行」ボタンを押してください。</li>
                                </ol>
                                <div style="margin:10px;"><span style="color:#C66;">（削除しないと第三者にインストールを実行される可能性があります）</span></div>
                              </div>
                              <div id="finish_ok" style="$style_default">
                                <div class="alert1"><span>このファイル「$self」は不要となるため、<br />
                                  自動で削除されました。</span></div>
                              </div>
                              <div id="finish_ex_bad" style="$style_default">
                                <div class="alert1"><span>【フォルダチェックエラー】<br>
                                  「$Exception_dir_name」フォルダのパーミッション（属性）変更が<br>
                                  自動処理できませんでした。</span></div>
                                <div style="margin:10px;">以下の作業をおこなってください。</div>
                                <ol>
                                  <li>FTPでログインし、「<span style="color:#C66;">$Exception_dir_name</span>」フォルダのパーミッション（属性）を[<span style="color:#C66;">705</span>]に手動変更してください。 </li>
                                  <br>
                                  <li>「再試行」ボタンを押してください。</li>
                                </ol>
                              </div></td>
                          </tr>
                          <tr>
                            <td class="td_color5"><input name="button" type="button" value="　セットアップ画面へ　" onClick="location.href = '$setup';" id="gotoSetup" />
                              <input name="button" type="button" value="　再試行　" onClick="atweb.installer.reconfirm();" id="reconfirmSetup" />
                              <input name="button" type="button" value="　再試行　" onClick="atweb.installer.delcofirm('$self');" id="delconfirmSetup" /></td>
                          </tr>
                        </table>
                      </div>
                    </div>
                  </div>
                  <div class="footer">
                    <div class="c"></div>
                  </div>
                </div></td>
            </tr>
          </table>
          <br />
        </div>
      </blockquote>
      <!-- powered -->
      <div id="layout_body_powered"> <img src="https://www.atmarkweb.jp/images/powered_by_atweb.png" style="float:right;" /> </div>
      <br style="clear:both;" />
      <!-- //powered --> 
    </div>
    <!-- //main --> 
    <!-- footer -->
    <div id="layout_footer">Copyright(C) RakuMail All rights reserved. </div>
    <!-- //footer --> 
  </div>
</div>
</body>
</html>
END

&show_exception($Exception_flag);



if( ! -w $install_base_dir || ! -w $install_datadir_base || ! -w $install_imgdir_base  || &chkDirformat($install_datadir) || &chkDirformat($install_imgdir) || &chkDirName($Exception_flag,$Exception_dir_name) ){
	
	if( ! $Exception_flag && $uid ){
		if( ! -w $install_base_dir ){
			# 設置フォルダ
			&inner_show('error_nosuexec');
			&show_exception(1);
		}else{
			
			if( &chkDirformat($install_datadir) ){
				&inner_show("error_datadir_format");
			}elsif( ! -d $install_datadir_base ){
				&inner_show("error_datadir_non");
			}elsif( ! -w $install_datadir_base ){
				&inner_show("error_dircheck");
			}
			
			
			if( &chkDirformat($install_imgdir) ){
				&inner_show("error_imgdir_format");
			}elsif( ! -d $install_imgdir_base ){
				&inner_show("error_imgdir_non");
			}elsif( ! -w $install_imgdir_base ){
				&inner_show("error_dircheck");
			}
		}
	}else{
		if( &chkDirName($Exception_flag,$Exception_dir_name) ){
			&inner_show("error_dirname_ex");
		}else{
			if( ! -w $install_base_dir ){
				# 設置フォルダ
				if( ! $Exception_flag ){
					&inner_show('error_suexec');
				}else{
					&inner_show('error_nosuexec_ex');
				}
			}
			
			if( $install_datadir_base ne $install_base_dir ){
				if( &chkDirformat($install_datadir) ){
					&inner_show("error_datadir_format");
				}elsif( ! -d $install_datadir_base ){
					&inner_show("error_datadir_non");
				}elsif( ! -w $install_datadir_base ){
					&inner_show("error_dircheck");
				}
			}
			
			if( $install_imgdir_base ne $install_base_dir ){
				if( &chkDirformat($install_imgdir) ){
					&inner_show("error_imgdir_format");
				}elsif( ! -d $install_imgdir_base ){
					&inner_show("error_imgdir_non");
				}elsif( ! -w $install_imgdir_base ){
					&inner_show("error_dircheck");
				}
			}
		}
	}
	
	&inner_show('install_error');
	&inner_show('install_ready');
	exit;
}elsif( $install_datadir_name eq '' || $install_imgdir_name eq '' ){
	if( $install_datadir_name eq '' ){
		&inner_show("error_datadir");
	}
	if( $install_imgdir_name eq '' ){
		&inner_show("error_imgdir");
	}
	&inner_show('install_error');
	&inner_show('install_ready');
	exit;
}else{
	#-------------------------------------------------------------
	# 開始画面
	#-------------------------------------------------------------
	&inner_show('install_ready');
	&inner_show('install_start');
	exit;
}


exit;
#-------------------------------------------
# 表示関連
#-------------------------------------------
sub inner_hide
{
	my( $elem ) = @_;
	print <<"JSH";
<script type="text/javascript"><!--
document.getElementById('$elem').style.display = "none";
// --></script>
JSH
}
sub inner_show
{
	my( $elem ) = @_;
	print <<"JSS";
<script type="text/javascript"><!--
document.getElementById('$elem').style.display = "";
// --></script>
JSS
}

sub inner_text
{
	my( $elem, $str ) = @_;
	print <<"JSI";
<script type="text/javascript"><!--
document.getElementById('$elem').innerHTML = "$str";
// --></script>
JSI
}

sub show_exception
{
	my $flag = shift;
	if( $flag ){
		print <<"JSEX";
<script type="text/javascript"><!--
\$("#restart").hide();
\$("#restart_ex").show();
\$("#restart_download").hide();
\$("#downstart").hide();
\$("#downstart_ex").show();
// --></script>
JSEX
	}else{
		print <<"JSEX";
<script type="text/javascript"><!--
\$("#restart").show();
\$("#restart_ex").hide();
\$("#restart_download").hide();
\$("#downstart").show();
\$("#downstart_ex").hide();
// --></script>
JSEX
	}
}


sub header_nocache
{
	print "Pragma: no-cache\n";
	print "Cache-Control: no-cache\n";
	print "Expires: Thu, 01 Dec 1994 16:00:00 GMT\n";
}
#----------------------------------------------------------------------#
#エラー処理（単体動作）
#	引数：エラーメッセージ
#	返り値：特になし
#	呼び出し例：&error("データ読み込みに失敗しました") ;
#		※メッセージを表示し、プログラムを終了する
#----------------------------------------------------------------------#
sub error {
	my $msg = shift;
	print <<"ERROR";
<div>$msg</div>
ERROR
}

# METHODの判定
sub method_ck
{
	my($all);
	unless($ENV{'REQUEST_METHOD'} eq 'POST'){
		$all= $ENV{'QUERY_STRING'};
		&get_param($all);
	}else{
		read(STDIN, $all, $ENV{'CONTENT_LENGTH'});
		&get_param($all);
	}
}

# 入力パラメータの解析
sub get_param{
	local($alldata) = @_;
	local($data, $key, $val);
	$alldata = $alldata || "";
	foreach $data (split(/&/, $alldata)){
		($key, $val) = split(/=/, $data);
		$key =~ tr/+/ /;
		$key =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C',hex($1))/eg;
		$key =~ s/\t//g;
		if( $val ){
			$val =~ tr/+/ /;
			$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack('C',hex($1))/eg;
			$val =~ s/\t//g;
		}
		$param{$key} = $val;
	}
}
sub get_self
{
	my $self = shift;
	my $path = $ENV{'SCRIPT_FILENAME'};
	if( $path && $path =~ /\/([^\/]+)$/ ){
		return $1;
	}
	return $self;
}
sub urlencode
{
	my $str = shift;
	$str =~ s/([^\w ])/'%' . unpack('H2', $1)/eg;
	$str =~ tr/ /+/;
	return $str;
}
sub get_resource
{
	my( $ref, $q, $opt ) = @_;
	my $handle = &connect($ref, $q );
	if( defined $ref->{'error'} ){
		return;
	}
	my $status = 0;
	while(<$handle>){
		if( /200/ ){
			$status = 1;
		}
		last if( /^[\r|\n]$/ );
	}
	if( ! $status ){
		$ref->{'error'} = "status";
		return;
	}
	
	my %func = (
		'list' => \&_resouce_array
	);
	if( $opt && defined $func{$opt} ){
		return $func{$opt}->($handle);
	}
	
	return &_resource_contents($handle);
}

sub _resouce_array
{
	my $handle = shift;
	my @data = ();
	while(<$handle>){
		chomp;
		push @data, $_;
	}
	return @data;
}

sub _resource_contents
{
	my $handle = shift;
	my $data = "";
	binmode($handle);
	while(<$handle>){
		$data .= $_;
	}
	return $data;
}

sub connect
{
	my( $ref, $q) = @_;
	my $host = 'www.atmarkweb.jp';
	my $path = 'cgi-bin/install/index.cgi';
	my $query = "";
	if( $q ){
		my @aq = ();
		foreach my $k ( keys %$q){
			push @aq, $k .'='.$q->{$k};
		}
		$query = '?'. join( '&', @aq );
	}
	
    my $port = getservbyname('http', 'tcp') || '80';
	my $handle = *SOCKET;
	
	#----------------接続処理-------------------
	
	# ホスト名を、IPアドレスの構造体に変換
	unless( $iaddr = inet_aton($host) ){
		$ref->{'error'} = "02";
		return;
	}
	
	# portとIPアドレスとまとめて構造体に変換
	$sock_addr = pack_sockaddr_in($port, $iaddr);
	
	# ソケット生成
	unless( socket($handle, PF_INET, SOCK_STREAM, 0) ){
		$ref->{'error'} = "03";
		return;
	}
	
	# 指定のホストの指定のportに接続
	unless( connect($handle, $sock_addr) ){
		close($handle);
		$ref->{'error'} = "04";
		return;
	}
	
	# ファイルハンドル$handleをバッファリングしない
	select($handle); $|=1; select(STDOUT);
	
	#------------HTTPリクエスト送信-----------------
	print $handle "GET /$path$query HTTP/1.0\r\n";
	print $handle "Host:$host\r\n";
	print $handle "\r\n";
	
	return $handle;

}

sub chkInstalldir
{
	my( $dir ) = @_;
	$dir =~ s/\/$//;
	my $base = '';
	my $install = '';
	
	my @d = split( /\//, $dir );
	if( $d[-1] =~ /^[^\.|\/]+$/ ){
		$install = pop @d;
		$base = join( "/", @d );
	}else{
		$base = $dir;
		$install = "";
	}
	$base = './' if( $base eq '' );
	$base .= '/' if( $base !~ /\/$/ );
	return $base,$install;
}

sub chkDirformat
{
	my( $dir ) = @_;
	
	if( $dir =~ /\/\// ){
		return 1;
	}
	if( $dir =~ /\.\.\./ ){
		return 1;
	}
	foreach my $name ( split(/\//,$dir ) ){
		if( $name =~ /\.[^\.]+$/ ){
			return 1;
		}
	}
	
}

sub chkDirName
{
	my( $flag, $dir ) = @_;
	
	if( ! $flag ){
		return 0;
	}
	if( $dir =~ /^\.\./ ){
		return 1;
	}
	$dir = &dirClean( $dir );
	if( $dir =~ /[\.\/\\]/ ){
		return 1;
	}
	return 0;
}

sub dirClean
{
	my $dir = shift;
	$dir =~ s/^[\.]//g;
	$dir =~ s/^[\/]//g;
	$dir =~ s/^[\\]//g;
	$dir =~ s/[\.]$//g;
	$dir =~ s/[\/]$//g;
	$dir =~ s/[\\]$//g;
	return $dir;
}

sub getPms
{
	my $file = shift;
	return substr( sprintf( "%03o", (stat($file))[2] ), -3 )
}

sub getPerlpath
{
	open( SELF, "<$self" );
	my $perlpath = <SELF>;
	close(SELF);
	$perlpath =~ s/\s+$//g;
	return $perlpath;
}

sub suExec
{
	my $path = shift;
	my $os = $^O;
	if($os !~ /MSWin32/i){
		my $execuid = $<;	#実UID
		my $owneruid = (stat($path))[4];
		if( $execuid eq "" || $owneruid eq "" ){
			return;
		}
		if($execuid eq $owneruid) {
			return;
		}
		return $owneruid;
	}else{
		return;
	}
	return;
}

sub chkChown
{
	my( $self, $path ) = @_;
	if( (stat($self))[4] ne (stat($path))[4] ){
		return 1;
	}
	return 0;
}

sub debug {
	($error,@error_fields) = @_;

	print "Content-type: text/html\n\n";
	print "<html><head><title>CGI</title></head>\n";
	print "<body>\n";
	print "$_[0]";
	print "</body></html>\n";
	exit;
}

