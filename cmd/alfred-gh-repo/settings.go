package main

type workFlowConfig struct {
	CacheTimeout int `json:"cache_timeout"`
}

func GetCacheTimeout() (int, error) {
	return 0, nil
}

func SetCacheTimeout(int) error {
	return nil
}
