import sys
from pyzotero import zotero
from diophila import OpenAlex
from loguru import logger

class ZoteroAbstractCompleter:
    def __init__(self, library_id, api_key):
        """
        初始化Zotero摘要补全器
        
        参数:
            library_id: Zotero用户ID或组ID
            api_key: Zotero API密钥
        """
        self.library_id = library_id
        self.api_key = api_key
        self.zot = zotero.Zotero(library_id, 'user', api_key)
        self.openalex = OpenAlex()
        
        # 配置日志
        logger.remove()
        logger.add(sys.stdout, level="INFO")
    
    def get_items_without_abstract(self):
        """获取所有没有摘要的文献条目"""
        try:
            # 获取所有文献条目
            items = self.zot.everything(self.zot.items())
            # 过滤出没有摘要的文献条目
            items_without_abstract = [
                item for item in items 
                if (item['data'].get('itemType') in ['journalArticle', 'conferencePaper', 'preprint']) 
                and (not item['data'].get('abstractNote'))
            ]
            logger.info(f"找到 {len(items_without_abstract)} 个没有摘要的文献条目")
            return items_without_abstract
        except Exception as e:
            logger.error(f"获取文献条目时出错: {e}")
            return []

    def get_openalex_abstract(self, doi):
        """
        从OpenAlex获取文献摘要
        
        参数:
            doi: 文献的DOI
        
        返回:
            成功返回摘要文本，失败返回None
        """
        try:
            if not doi:
                return None
                
            work = self.openalex.get_single_work(f"https://doi.org/{doi}", "doi")
            if not work or 'abstract_inverted_index' not in work:
                return None
                
            # 将abstract_inverted_index转换为正常文本
            abstract_inverted_index = work['abstract_inverted_index']
            word_positions = {}
            
            # 为每个单词的每个位置创建映射
            for word, positions in abstract_inverted_index.items():
                for position in positions:
                    word_positions[position] = word
            
            # 按位置顺序排列单词
            if not word_positions:
                return None
                
            max_position = max(word_positions.keys())
            abstract_text = []
            for i in range(max_position + 1):
                if i in word_positions:
                    abstract_text.append(word_positions[i])
            
            return " ".join(abstract_text)
            
        except Exception as e:
            logger.error(f"从OpenAlex获取摘要时出错: {e}")
            return None

    def add_note_to_item(self, item_key, note_text):
        """
        为文献添加笔记
        
        参数:
            item_key: 文献条目的key
            note_text: 笔记内容
        """
        try:
            template = {
                'itemType': 'note',
                'parentItem': item_key,
                'note': note_text
            }
            self.zot.create_items([template])
            logger.info(f"已为文献 {item_key} 添加笔记")
        except Exception as e:
            logger.error(f"添加笔记时出错: {e}")

    def update_item_abstract(self, item_key, abstract):
        """
        更新文献的摘要
        
        参数:
            item_key: 文献条目的key
            abstract: 新的摘要内容
        """
        try:
            item = self.zot.item(item_key)
            item['data']['abstractNote'] = abstract
            self.zot.update_item(item)
            logger.info(f"已更新文献 {item_key} 的摘要")
        except Exception as e:
            logger.error(f"更新摘要时出错: {e}")

    def add_tag_to_item(self, item_key, tag):
        """
        为文献添加标签
        
        参数:
            item_key: 文献条目的key
            tag: 标签内容
        """
        try:
            item = self.zot.item(item_key)
            # 获取现有标签
            tags = item['data'].get('tags', [])
            # 添加新标签
            tags.append({'tag': tag})
            item['data']['tags'] = tags
            # 更新条目
            self.zot.update_item(item)
            logger.info(f"已为文献 {item_key} 添加标签: {tag}")
        except Exception as e:
            logger.error(f"添加标签时出错: {e}")

    def complete_abstracts(self):
        """补全所有缺失的摘要"""
        items = self.get_items_without_abstract()
        
        for item in items:
            item_key = item['key']
            doi = item['data'].get('DOI')
            title = item['data'].get('title', '未知标题')
            
            logger.info(f"正在处理文献: {title}")
            
            if not doi:
                logger.warning(f"文献 '{title}' 没有DOI")
                self.add_note_to_item(
                    item_key,
                    "⚠️ 此文献缺少摘要且没有DOI，请手动补充摘要。"
                )
                self.add_tag_to_item(item_key, "需要手动补充摘要")
                continue
            
            abstract = self.get_openalex_abstract(doi)
            
            if abstract:
                self.update_item_abstract(item_key, abstract)
                logger.info(f"成功为文献 '{title}' 补充摘要")
            else:
                logger.warning(f"无法从OpenAlex获取文献 '{title}' 的摘要")
                self.add_note_to_item(
                    item_key,
                    "⚠️ 无法从OpenAlex获取摘要，请手动补充。"
                )
                self.add_tag_to_item(item_key, "需要手动补充摘要")

def main():
    """主函数"""
    # 在这里填写你的Zotero信息
    ZOTERO_ID = "16076403"
    ZOTERO_KEY = "ETem7u5Vn5TAVNARb6Djj4Kq"
    
    completer = ZoteroAbstractCompleter(ZOTERO_ID, ZOTERO_KEY)
    completer.complete_abstracts()

if __name__ == "__main__":
    main() 