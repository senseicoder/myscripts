<?php

define('formeCLI', 'cli');
define('formeJSON', 'json');


function AnalysesSQL($oDB, array $aAnalyses, $bDebug = FALSE, $sForme = formeCLI)
{
	$sOut = '';
	$aTab = array();

	foreach($aAnalyses as $sLib => $sSQL) if( ! empty($sSQL)) {
		$aResult = $oDB->Query($sSQL);
		if($bDebug) printf("=== SQL: %s\n", $sSQL);
		if(count($aResult)) {
			$aDisplay = array();
			foreach($aResult as $aRec) $aDisplay[] = trim($aRec['lib']);
			switch($sForme)
			{
				case formeCLI: 
					foreach($aDisplay as & $sValue) $sValue = ' * ' . $sValue;
					$sOut .= sprintf("%s :\n%s\n", $sLib, implode("\n", $aDisplay)); 
					break;	
				case formeJSON: 
					foreach($aDisplay as $sValue) {
						$aExp = explode(' : ', $sValue);
						$sUser = $aExp[0];
						$sHosts = isset($aExp[1]) ? $aExp[1] : '';
						$aTab[$sLib][$sUser] = explode(',', $sHosts);
					}
					break;	
				default: die('forme non gérée : ' . $sForme);
			}
		}
	}

	switch($sForme)
	{
		case formeCLI: echo $sOut; break;	
		case formeJSON: echo json_encode($aTab); break;	
		default: die('forme non gérée : ' . $sForme);
	}	
}

function RecodagesSQL($oDB, array $aAnalyses)
{
	foreach($aAnalyses as $sSQL) {
		$oDB->Exec($sSQL);
	}
}