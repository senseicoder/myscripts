<?php

class CDB
{
	private $mysqli;

	function __construct($dbHost, $dbLogin, $dbPassword, $dbBase)
	{
		$this->mysqli = new mysqli($dbHost, $dbLogin, $dbPassword, $dbBase);
		if ($this->mysqli->connect_error) die('Erreur de connexion (' . $this->mysqli->connect_errno . ') ' . $mysqli->connect_error);
		$this->mysqli->set_charset("utf8");
	}

	function __destruct()
	{
		$this->mysqli->close();
	}

	function Exec($sSQL)
	{
		if($this->mysqli->query($sSQL) !== TRUE) {
			die(sprintf("erreur '%s' pour: %s\n", $this->mysqli->error, $sSQL));
		}		
	}

	function Query($sSQL)
	{
		if($result = $this->mysqli->query($sSQL)) {
			$aResult = array();
			while ($row = $result->fetch_assoc()) $aResult[] = $row;
			return $aResult;			
		}
		else {
			die(sprintf("erreur '%s' pour: %s\n", $this->mysqli->error, $sSQL));
		}
	}

	function Recreate($sTableName, array $aFields)
	{
		$this->Exec('drop table if exists ' . $sTableName);
		$sSQL = sprintf('create table %s(%s)', $sTableName, implode(',', $aFields));
		$this->Exec($sSQL);
	}

	function ReCreateDatabase($sDBName)
	{
		$this->Exec('drop database if exists ' . $sDBName);
		$sSQL = sprintf('create database %s', $sDBName);
		$this->Exec($sSQL);		
	}

	function Array2Table($sNom, array $aData)
	{
		$aChamps = array_keys($aData[0]);
		$aChampsCreate = array();
		foreach($aChamps as $sChamp) {
			$aChampsCreate[] = sprintf('%s VARCHAR(255)', $sChamp);
		}

		$nb = 0;
		$sTable = $sNom;
		$this->Recreate($sTable, $aChampsCreate);
		foreach($aData as $aLine) {
			$aValues = array();
			foreach($aLine as $sValue) {
				$aValues[] = sprintf('"%s"', $sValue);
			}
			$this->Exec(sprintf('insert into %s(%s) values(%s)', $sTable, implode(',', $aChamps), implode(',', $aValues)));
			$nb++;
		}		
		return $nb;
	}
}
